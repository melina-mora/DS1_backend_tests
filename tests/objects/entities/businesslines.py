from objects.api.config import ConfigBusinessLines


class BusinessLines:
    def __init__(self, user):
        self._config_business_lines = ConfigBusinessLines().configure_test_data_business_lines()

        self._user = user

    #region Get information
    def get_config_from_opportunity(self, opportunity=None):
        apis = self._config_business_lines["usp_sm_GetOpportunities_ByOpportunityId_BusinessLines_v6"]

        if opportunity is not None:
            url = opportunity.json()
            url = url["links"]["configuration"]
        else:
            raise ValueError('Missing parameters: opportunity')

        r = self._user.get(url=url)
        business_lines_config = r["businessLines"]["businessLineId"]
        return r


    def fetch_business_lines_configuration(self, user, opportunity):
        business_lines = BusinessLines(user)
        opportunity = business_lines.get_config_from_opportunity(opportunity=opportunity)
        return opportunity
    #endregion
    #region Set information
    def set_business_lines_payload(self, opportunity, *business_lines):
        bls = []
        key = 'businessLineId'

    #endregion
    #region Validations
    def validate_business_lines(self, opportunity=None):
        config = self.get_config_from_opportunity(opportunity=opportunity) #Config from opp
        config_business_lines = config["businessLines"]["businessLineId"] #Config for customer

        if len(config_business_lines) != 0:
            assert True
        else:
            assert False, "Opportunity doesn't have access, configuration: %s" % config_business_lines
    #endregion