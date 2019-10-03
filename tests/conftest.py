from copy import deepcopy
from json import loads
from pathlib import Path

from pytest import fixture

from tests.config import Config
from tools.json_tools import extract


# region Commands for terminal to use along with pytest
@fixture(scope='session')
def env(request):
    return request.config.getoption('--env')


@fixture(scope='session')
def testdata(request):
    return request.config.getoption('--testdata')


def pytest_addoption(parser):
    parser.addoption('--env',
                     action='store',
                     help='Environment to run the tests against. Example: "dev".',
                     default='dev')

    parser.addoption('--testdata',
                     action='store_true',
                     help='''
                     Update/create new test data with the file provided. Must specify path to the file
                     to extract data from. Data should be .csv format.
                     Data must contain in the following order: ENV, USER, PSWD, Int/Ext, COUNTRY.
                     ''')
# endregion

# region Global configuration for pytest runs


@fixture(scope='session')
def app_config(env):
    cfg = Config(env)
    return cfg


def update_test_data(testdata):
    file = testdata if testdata else None
    try:
        if file:
            file.prepare_test_data(filename=file)
            print('Data has been updated!')
        else:
            print('Data didn\'t get updated, using existing files...')
    except Exception:
        print('Could not update test data, using actual values...')
        pass
# endregion

# region Test data files configuration for each test script called by working directory. Example: Credentials.


@fixture(scope="function")
def project_document_data(request):
    def load_project_document_data(data):
        d = data
        f = Path(request.node.fspath.strpath)
        d = f.with_name("project.pdf")
        return d

    return load_project_document_data


@fixture(scope="function")
def load_test_data(env, data_config):
    def load_test_data_env(country, is_crm=False, is_bso=False):
        data = deepcopy(data_config)
        if is_crm:
            # Extract data to integrate to CRM.
            path = '$.%s[?(@.IsCRM==true&@.country=="%s")]' % (env, country)
        elif is_bso:
            # Extract data for BSO user.
            path = '$.%s[?(@.IsBSO==true&@.country=="%s")]' % (env, country)
        elif country:
            # Extract data for specific country.
            path = '$.%s[?(@.country == "%s")]' % (env, country)
        else:
            raise ValueError("Error occurred while evaluating is_crm/is_bso flag/country.")

        data = extract(body=data, path=path)
        return data
    return load_test_data_env


@fixture(scope="class")
def data_config(request, env):
    f = Path(request.node.fspath.strpath)
    config = f.with_name("data.json")
    with config.open() as fd:
        test_data = loads(fd.read())
    yield test_data


def pytest_generate_tests(metafunc):
    if 'data_config' not in metafunc.fixturenames:
        return
    config = Path(metafunc.module.__file__).with_name('data.json')
    test_data = loads(config.read_text())
    param = test_data.get(metafunc.function.__name__, None)
    if isinstance(param, list):
        metafunc.parametrize('data_config', param)
# endregion
