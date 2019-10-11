from scripts.mongo_tools_script.mongo_connection import MongoDBConnection
from tools.json_tools import extract


class Config:
    def __init__(self, env, layer):
        self._config = MongoDBConnection(db='TestData', coll='Environments')
        self.env = env
        self.base_url = self.configure_environment(env, layer)

    def configure_environment(self, env, layer):
        env_object = self._config.coll.find_one({'name': env})
        base_url = extract(body=env_object, path='$.%s' % layer)
        return base_url
