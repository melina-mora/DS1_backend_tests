from datetime import datetime
from warnings import warn

from data_test.database_connection import DatabaseConn
from objects.entities.opportunity.opportunity import Opportunity
from tools.json_tools import *


class OpportunityAddressRequest(Opportunity):

    def __init__(self, user, code):
        super().__init__(user, code)
        self._user = user
        self._code = code
        self._config = super().set_opp_config()
        self._conn = DatabaseConn(db='TestData', coll='Addresses')

    def patch_opportunity_address(self, opportunity=None, opportunity_id=None, payload=None, title=None):
        apis = self._config["usp_sm_PatchOpportunityById_v5"]
        payload = self._conn.coll.find_one({'country': self._user.get_user_country(), })

        if opportunity is None and opportunity_id is not None:
            url = "%s%s" % (extract(body=apis, path="$.url"), str(opportunity_id))
            opportunity = self._user.get(url=url)
        elif opportunity is not None:
            url = extract(body=opportunity.json(), path="$.links.self")
        else:
            raise ValueError("Missing parameters: opportunity or opportunity_id")

        payload = self.set_address(opportunity=opportunity, body=payload, title=title)
        r = self._user.patch(url=url, payload=payload)
        return r

    def set_address(self, opportunity, body, title=None):
        # Fetch user's country:
        user_country = self._user.get_user_country()

        # Set opportunity description:
        if not title:
            opp_title = "aut_test_%s" % datetime.now().strftime("DS1_%Y%m%d_%H%M")
        else:
            opp_title = title

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
