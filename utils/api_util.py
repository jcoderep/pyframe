
import json
import requests
from utils.assertions import *
from lxml import etree


def parse_html_to_list(html_content):
    """ """
    try:
        parsed_data = []
        table = etree.HTML(html_content).find("body/table")  # type: ignore
        rows = iter(table)
        headers = [col.text for col in next(rows)]
        for row in rows:
            values = [json.loads(col[len(col.getchildren())-1].text) if col.getchildren() else col.text for col in row]
            parsed_data.append(dict(zip(headers, values)))
        return parsed_data
    except Exception as exp:
        raise exp


class APIUtil:
    """ """
    def __init__(self, server_url, headers=None):
        """ """
        self.server_url = server_url
        if headers:
            self.headers = headers
        else:
            self.headers = {"Accept": "Application/json"}

    def execute_get(self):
        """ """
        try:
            response = requests.get(self.server_url, headers=self.headers, verify=False)
            if not assert_equal(response.status_code, 200):
                raise Exception('The GEt API failed to fetch response and returned with status code {}'.format(
                    response.status_code))
            try:
                parsed_response = json.loads(response.content)
            except json.decoder.JSONDecodeError:
                parsed_response = parse_html_to_list(response.content)
                return parsed_response
            return parsed_response
        except Exception as exp:
            raise exp

    def execute_post(self, params):
        """ """
        try:
            response = requests.post(self.server_url, headers=self.headers, json=param, verify=False)
            if not assert_equal(response.status_code, 200):
                raise Exception('The GEt API failed to fetch response and returned with status code {}'.format(
                    response.status_code))
            try:
                parsed_response = json.loads(response.content)
            except json.decoder.JSONDecodeError:
                parsed_response = parse_html_to_list(response.content)
                return parsed_response
            return parsed_response
        except Exception as exp:
            raise exp

    def execute_put(self, params):
        """ """
        try:
            response = requests.put(self.server_url, headers=self.headers, json=params, verify=False)
            if not assert_equal(response.status_code, 200):
                raise Exception('The GEt API failed to fetch response and returned with status code {}'.format(
                    response.status_code))
            try:
                parsed_response = json.loads(response.content)
            except json.decoder.JSONDecodeError:
                parsed_response = parse_html_to_list(response.content)
                return parsed_response
            return parsed_response
        except Exception as exp:
            raise exp
