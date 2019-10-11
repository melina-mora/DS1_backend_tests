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


class CountriesConfig:

    def __init__(self, env):
        self.env = env

    def load_countries_config_by_feature(self, features_list):
        features = MongoDBConnection(db='TestData', coll='Features')

        country_config = list(features.coll.find({'feature': {'$in': features_list}}))
        countries = []

        for i in country_config:
            i = extract(body=i, path='$.countries.%s' % self.env)
            countries = countries + i

        countries = list(set(countries))
        print('Countries configured by features combination: %s, countries: %s' % (features_list, countries))
        return countries
