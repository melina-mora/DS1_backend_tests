class Config:
    def __init__(self, env):
        self.env = env
        self.base_url = self.configure_environment(env)

    def configure_environment(self, env):
        '''
        SUPPORTED_ENVS = Constant that should handle all environments available to run the test suites. The
        default language is 'debug', which allows to run the test cases in local to debug. The '_ds' environments
        are for .NET layer, while without is for API management.
        '''
        SUPPORTED_ENVS = ['dev', 'dev2', 'qa', 'preprod', 'prod'] + ['dev_ds', 'dev2_ds', 'qa_ds', 'preprod_ds',
                                                                     'prod_ds']

        if env not in SUPPORTED_ENVS:  # TODO refactor, this should be handled in other way
            raise Exception('%s not supported. \n List of supported environments: %s' % (env, SUPPORTED_ENVS))

        if '_ds' not in env[0:-3]:
            base_url = {
                'dev': 'https://uscldcnxapmd01.azure-api.net',
                'dev2': 'https://uscldcnxapmsa01.azure-api.net',
                'qa': 'https://qa.cemexgo.com/api',
                'preprod': 'https://uscldcnxapmpp01.azure-api.net',
                # 'prod': 'https://cemex.azure-api.net'
            }[env]
        else:
            base_url = {  # TODO confirm these urls
                'dev_ds': 'https://uscldcnxapid01.azure-api.net',
                'dev2_ds': 'https://uscldcnxapmsa01.azure-api.net',
                'qa_ds': 'https://uscldcnxapiq01.azurewebsites.net',
                'preprod_ds': 'https://uscldcnxapipp01.azurewebsites.net',
                # 'prod_ds': 'https://uscldcnxapip01.azurewebsites.net'
            }[env]

        return base_url
