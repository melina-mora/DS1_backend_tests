from objects.entities.opportunity.opportunity_business_lines import OpportunityBusinessLines
from objects.entities.opportunity.opportunity_address_request import OpportunityAddressRequest
from objects.entities.opportunity.opportunity_contact_request import OpportunityContactRequest

from tools.json_tools import extract


class JobsiteRequest(OpportunityBusinessLines, OpportunityAddressRequest, OpportunityContactRequest):
    def __init__(self, user, code):
        self._user = user
        self._code = code
        self._id = None
        super().__init__(user, code)

    def post_new(self, legal_entity_id=None, payload=None):
        r = self.post_new_opportunity(legal_entity_id=legal_entity_id, payload=payload)
        self._id = extract(body=r.json(), path="$..opportunityId")
        return r

    def get_jobsite_request_by_ids(self, opportunity=None, opportunity_id=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")

        r = self.get_opportunity_by_id(opportunity=opportunity, opportunity_id=opportunity_id)
        return r

    def patch_request_address(self, opportunity=None, opportunity_id=None, payload=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")
        r = self.patch_opportunity_address(opportunity=opportunity, opportunity_id=opportunity_id, payload=payload)
        return r

    def put_business_lines(self, opportunity=None, opportunity_id=None, payload=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")
        r = self.put_opportunity_business_lines(opportunity=opportunity, opportunity_id=opportunity_id, payload=payload)
        return r

    def put_contact_request(self, opportunity=None, opportunity_id=None, payload=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")
        r = self.put_opportunity_contact_request(opportunity=opportunity, opportunity_id=opportunity_id, payload=payload)
        return r
