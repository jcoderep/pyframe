
import json
import pytest

from configs.user_constants import  TMP_CMD_LINE_ARGS_JSON
from utils.reporting_util import Reporting
from utils.common import read_input_data


def pytest_addoption(parser):
    """ """
    parser.addoption('--environment', actions='store', default='UAT', help='Environment for the test execution')
    parser.addoption('--browser', actions='store', default='Chrome', help='Browser for the test execution')
    parser.addoption('--test_type', actions='store', default='System', help='Test type for run configuration')
    parser.addoption('--test_sub_type', actions='store', default='Sanity', help='Test sub-type for run configuration')
    parser.addoption('--application', actions='store', default='TestApp', help='Application under test')
    parser.addoption('--run_type', actions='store', default='UI', help='Execution type - UI/API')
    parser.addoption('--skip_list', actions='store', default='', help='List of test cases to be skipped')


def pytest_collection_modifyitems(config, items):
    """ """
    tests_to_skip = config.getoption('--skip_list')
    if not tests_to_skip:
        return
    skip_listed = pytest.mark.skip(reason='Included in the skiplist through cmd line')
    for item in items:
        if item.name.split('[')[0] in tests_to_skip:
            item.add_marker(skip_listed)


def pytest_generate_tests(metafunc):
    """ """
    if 'data' in metafunc.fixturenames:
        metafunc.parameterize('data', read_input_data(
            metafunc.config.option.environment, metafunc.config.option.test_sub_type)
        )


@pytest.fixture(scope='class')
def cmd_line_args(request):
    """ Fixture to initialize commad line arguments """
    request.cls.args = {
        'environment': request.config.getoption('--environment'),
        'browser': request.config.getoption('--browser'),
        'test_type': request.config.getoption('--test_type'),
        'test_sub_type': request.config.getoption('--test_sub_type'),
        'application': request.config.getoption('--application'),
        'run_type': request.config.getoption('--run_type')
    }

    with open(TMP_CMD_LINE_ARGS_JSON, 'w') as f:
        json.dump(request.cls.args, f)

    return request.cls.args


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish():
    """ """
    with open(TMP_CMD_LINE_ARGS_JSON, 'r') as f:
        args = json.loads(f.read())

    Reporting().send_bulk_scenario_data_to_elk(
        args['application'],
        args['test_type'],
        args['test_sub_type'],
        args['run_type'],
        args['environment'],
    )

    Reporting().send_overall_job_status_to_elk(
        args['application'],
        args['test_type'],
        args['test_sub_type'],
        args['run_type'],
        args['environment'],
    )