from pytest import fixture
from tests.config import Config
from json import loads
from pathlib import Path
from copy import deepcopy
from tools.json_tools import extract
from tools.exceptions import DataError


#region Commands for terminal to use along with pytest
def pytest_addoption(parser):
    parser.addoption('--env',
                     action='store',
                     help='Environment to run the tests against. Example: "dev".',
                     default='dev')


@fixture(scope='session')
def env(request):
    return request.config.getoption('--env')

#endregion

#region Global configuration for pytest runs
@fixture(scope='session')
def app_config(env):
    cfg = Config(env)
    return cfg

#endregion

#region Test data files configuration for each test script called by working directory. Example: Credentials.
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
    def load_test_data_env(is_crm=False, country=None):
        data = deepcopy(data_config)
        if is_crm:
            if country:
                # Extract data to integrate to CRM.
                path = '$.%s[?(@.IsCRM==true&@.country=="%s")]' % (env, country)
                data = extract(body=data, path=path)
            else:
                raise DataError("Must specify country value to integrate to CRM explicitly.")
        elif country and not is_crm:
            # Extract data to integrate to specific country.
            data = extract(body=data, path='$.%s[?(@.country == "%s")]' % (env, country))
        else:
            # Extract first test data available.
            data = extract(body=data, path='$.%s' % env)
            data = data if type(data) != list else data[0]
        return data
    return load_test_data_env()


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
#endregion