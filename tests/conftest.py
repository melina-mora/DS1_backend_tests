from pytest import fixture
from tests.config import Config
from json import loads
from pathlib import Path


#region Commands for terminal to use along with pytest
def pytest_addoption(parser):
    parser.addoption('--env',
                     action='store',
                     help='Environment to run the tests against. Example: "dev".',
                     default='debug')

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
def load_test_data(env, data_config):
    data = data_config
    return data[env]

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