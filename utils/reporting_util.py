
import os
import json
import uuid
import requests
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from configs.user_constants import PYTEST_JSON


class Reporting:
    """ """

    def __init__(self):
        """ """
        self.client = Elasticsearch([{"host": "10.80.79.86", "port": 9200, "scheme": "http"}])
        self.scenario_index = "bps_scenario_index"
        self.job_index = "bps_job_index"

    def check_if_index_exists_in_elk(self, index_name):
        """ """
        try:
            return self.client.indices.exists(index=index_name)
        except Exception as exp:
            raise exp

    def create_elk_index(self, index_name):
        """ """
        try:
            if not self.check_if_index_exists_in_elk(index_name):
                response = self.client.indices.exists(index=index_name)
                if not response['acknowledged']:
                    exp = "The ELK Index creation failed"
                    raise exp
                else:
                    pass
        except Exception as exp:
            raise exp

    @staticmethod
    def get_data_from_file(filepath):
        """ """
        try:
            with open(filepath, 'r') as f:
                data = [json.loads(d.strip()) for d in f]
            return data
        except Exception as exp:
            raise exp

    def bulk_json_data(self, index, application, test_type, test_sub_type, run_type, environment):
        """ """
        try:
            final_data = list()
            result_set_dict = self.get_data_from_file(PYTEST_JSON)
            for test in result_set_dict['tests']:
                upload_data = dict()
                if test.get('call'):
                    upload_data['duration'] = test['setup']['duration'] + test['call']['duration'] + \
                                              test['teardown']['duration']
                else:
                    upload_data['duration'] = test['setup']['duration'] + test['teardown']['duration']

                upload_data['date'] = datetime.now()
                upload_data['run_date'] = datetime.now()

                if test.get('call'):
                    upload_data['status'] = test['call']['outcome']
                else:
                    upload_data['status'] = 'passed'

                upload_data['run_id'] = uuid.uuid4()
                upload_data['application'] = application
                upload_data['test_type'] = test_type
                upload_data['test_sub_type'] = test_sub_type
                upload_data['run_type'] = run_type
                upload_data['_index'] = index
                upload_data['environment'] = environment
                final_data.append(upload_data)

            for doc in final_data:
                yield doc

        except Exception as exp:
            raise exp

    def send_overall_job_status_to_elk(self, application, test_type, test_sub_type, run_type, environment):
        """ """
        try:
            result_set_dict = self.get_data_from_file(PYTEST_JSON)[0]
            upload_data = dict()
            upload_data['duration'] = result_set_dict['duration']
            upload_data['date'] = datetime.now()
            upload_data['run_date'] = datetime.now()
            upload_data['pass_percentage'] = round(((result_set_dict['summary'].get('passed', 0) +
                                                   result_set_dict['summary'].get('skipped', 0)) /
                                                   result_set_dict['summary']['total'])*100)
            if upload_data['pass_percentage'] > 90:
                upload_data['status'] = 'passed'
            else:
                upload_data['status'] = 'failed'

            upload_data['run_id'] = uuid.uuid4().hex
            upload_data['application'] = application
            upload_data['test_type'] = test_type
            upload_data['test_sub_type'] = test_sub_type
            upload_data['run_type'] = run_type
            upload_data['environment'] = environment

            self.create_elk_index(self.job_index)
            headers = {'Content-Type': 'application/json'}
            uri = "http://10.80.79.86:9200" + self.job_index + "/_doc/?pretty"
            response = requests.post(uri, headers=headers, json=upload_data)
            if response.status_code != 201:
                exp = "Data upload failed with error" + json.loads(response.content)['error']['reason']
                os.remove(PYTEST_JSON)
                raise exp
            else:
                print('ELK job data uploaded successfully.')
                os.remove(PYTEST_JSON)
        except Exception as exp:
            raise exp

    def send_bulk_scenario_data_to_elk(self, application, test_type, test_sub_type, run_type, environment):
        """ """
        try:
            self.create_elk_index(self.scenario_index)
            response = helpers.bulk(self.client, self.bulk_json_data(self.scenario_index, application, test_type,
                                                                     test_sub_type, run_type, environment))
            if not response[0]:
                exp = "JSON content bulk upload failed"
                raise exp
            else:
                print('ELK scenario data uploaded successfully')
        except Exception as exp:
            raise exp
