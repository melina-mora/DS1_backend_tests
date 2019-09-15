from objects.entities.opportunity.opportunity import Opportunity
from tools.json_tools import *
from warnings import warn
from datetime import datetime


class OpportunityAddressRequest(Opportunity):

    def __init__(self, user, code):
        super().__init__(user, code)
        self._user = user
        self._code = code
        self._config = super().set_opp_config()

    def patch_opportunity_address(self, opportunity=None, opportunity_id=None, body=None):
        apis = self._config["usp_sm_PatchOpportunityById_v5"]

        if opportunity is None and opportunity_id is not None:
            url = extract(body=apis, path="$.url") + str(opportunity_id)
            opportunity = self._user.get(url=url)
        elif opportunity is not None:
            url = extract(body=opportunity.json(), path="$.links.self")
        else:
            raise ValueError("Missing parameters: opportunity or opportunity_id")

        body = self.set_address(opportunity=opportunity, body=body)
        r = self._user.patch(url=url, json=body)
        return r

    def set_address(self, opportunity, body):
        # Fetch user's country:
        user_country = self._user.get_user_country()

        # Set opportunity description:
        opp_title = "aut_test_%s" % datetime.now().strftime("DS1_%Y%m%d_%H%M")

        # Validate region or fetch the first one of the ones available:
        selected_region = extract(body=body, path="$.addressRequest.regionId")
        url = extract(body=opportunity.json(), path="$.addressRequest.links.regions")
        r = self._user.get(url=url)
        region_list = extract(body=r.json(), path="$..regionId", multiple=True)

        if selected_region not in region_list:
            warn(UserWarning(
                "%s not in regions available, set %s instead. Check test data." % (selected_region, region_list[0])))
            selected_region = region_list[0]

        # Now update the whole payload:
        body = update_json(body=body, values={
            "$.addressRequest.regionId": selected_region,
            "$.opportunityDesc": opp_title,
            "$.addressRequest.countryCode": user_country
        })

        return body
