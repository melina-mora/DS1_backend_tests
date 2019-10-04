from tests.data_test.database_connection import DatabaseConn
from tools.json_tools import extract



class Config:
    def __init__(self, env):
        self._config = DatabaseConn(db='TestData', coll='Environments')
        self.env = env
        self.base_url = self.configure_environment(env)

    def configure_environment(self, env):
        if '_ds' not in env[0:-3]:
            cursor = self._config.coll.find({'apim':'dev'})
            for i in cursor:
                print(i)
            base_url = extract(body=self._config.coll.find(), path='$.apim.%s' % env)
        else:
            base_url = extract(body=self._config.coll, path='$.ds.%s' % env.rstrip('_ds'))

        return base_url
