from objects.entities.opportunity.opportunity_address_request import OpportunityAddressRequest
from objects.entities.opportunity.opportunity_business_lines import OpportunityBusinessLines
from objects.entities.opportunity.opportunity_contact_request import OpportunityContactRequest
from objects.entities.opportunity.opportunity_document import OpportunityDocument
from tools.json_tools import extract


class JobsiteRequest(OpportunityBusinessLines, OpportunityAddressRequest, OpportunityContactRequest,
                     OpportunityDocument):
    def __init__(self, user):
        self._user = user
        self._code = 'R'
        self._id = None
        super().__init__(user, self._code)

    def get_jobsite_request_by_ids(self, opportunity=None, opportunity_id=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")

        r = self.get_opportunity_by_id(opportunity=opportunity, opportunity_id=opportunity_id)
        return r

    def post_new(self, legal_entity_id=None, payload=None):
        r = self.post_new_opportunity(legal_entity_id=legal_entity_id, payload=payload)
        self._id = extract(body=r.json(), path="$..opportunityId")
        return r

    def patch_request_address(self, opportunity=None, opportunity_id=None, payload=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")
        r = self.patch_opportunity_address(opportunity=opportunity, opportunity_id=opportunity_id, payload=payload)
        return r

    def patch_taxable_document(self, opportunity=None, opportunity_id=None, file=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")

        self.patch_opportunity_document(opportunity=opportunity,
                                        opportunity_id=opportunity_id,
                                        document_type="Taxable",
                                        file=file)
        r = self.get_opportunity_by_id(opportunity=opportunity, opportunity_id=opportunity_id)

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
