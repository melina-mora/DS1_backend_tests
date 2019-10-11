from pathlib import Path

from pytest import fixture, skip

from scripts.mongo_tools_script.mongo_connection import MongoDBConnection
from tests.config import Config


# region Commands for terminal to use along with pytest
@fixture(scope='session')
def env(request):
    return request.config.getoption('--env')


@fixture(scope='session')
def layer(request):
    return request.config.getoption('--layer')


@fixture(scope='session')
def testdata(request):
    return request.config.getoption('--testdata')


def pytest_addoption(parser):
    parser.addoption('--env',
                     action='store',
                     help='Environment to run the tests against. Example: "dev".',
                     default='dev')

    parser.addoption('--layer',
                     action='store',
                     help='Layer to run the tests against. Example: "ds", "apim".',
                     default='apim')
# endregion

# region Global configuration for pytest runs


@fixture(scope='session')
def app_config(env, layer):
    cfg = Config(env, layer)
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
def load_document_data(request):
    def load_document_data_file(file='test_document.pdf'):
        filepath = Path(request.node.fspath.strpath)
        if file:
            doc = filepath.with_name(file)
            return doc
        else:
            raise ('Must specify test file to use.')

    return load_document_data_file


@fixture(scope="function")
def load_test_user(env):
    def load_test_user_env(country, user_type):
        users = MongoDBConnection(db='TestData', coll='Users')
        types = MongoDBConnection(db='TestData', coll='UserTypes')

        user_type = types.coll.find_one({'type': user_type})
        user = users.coll.find_one({'user_type.$id': user_type['_id'],
                                    'env': env,
                                    'country': country})
        if not user:
            skip('User not found, check test data in DB. User required: %s|%s|%s' %
                 (env, country, user_type['type']))

        return user

    return load_test_user_env

# endregion
