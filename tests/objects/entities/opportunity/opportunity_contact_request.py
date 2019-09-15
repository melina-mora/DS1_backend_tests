from objects.entities.opportunity.opportunity import Opportunity
from tools.json_tools import *
from warnings import warn
from copy import deepcopy
from enum import Enum


class OpportunityContactRequest(Opportunity):

    def __init__(self, user, code):
        super().__init__(user, code)
        self._user = user
        self._code = code
        self._config = super().set_opp_config()

    def put_opportunity_contact_request(self, opportunity=None, opportunity_id=None, body=None):
        # Fetch opportunity
        if not opportunity and opportunity_id:
            opportunity = self.get_opportunity_by_id(opportunity_id=opportunity_id)
        elif not opportunity and not opportunity_id:
            raise ValueError("Missing parameters: opportunity or opportunity_id")

        # Extract url for adding
        url = extract(body=opportunity.json(), path='$.links.addContactRequests')
        if not url:
            assert False, "addContactRequests link is not present"

        # Set payload
        body = self.set_contact_request_data(body=body)

        response = self._user.put(url=url, json=body)
        return response

    def set_contact_request_data(self, body=None):
        apis = self._config['usp_sm_PatchOpportunityContactRequestById_v5']

        if body is None:
            raise ValueError("Must specify data for contact, check test data. Body:\n %s \n" % body)
        else:
            payload = extract(body=apis, path='$.body')
            c_type = self.calculate_contact_request_type(body=body)
            c_country = self._user.get_user_country()

            payload = update_json(body=payload, values={
                "$...name": extract(body=body, path='$..name'),
                "$...countryAreaCode": c_country,
                "$...phone": extract(body=body, path='$..phone'),
                "$...extension": extract(body=body, path='$..extension'),
                "$...email": extract(body=body, path='$..email'),
                "$...contactRequestType.contactRequestTypeId": c_type,
                "$..contactRole.contactPersonRoleId": 0, #TODO calculate role
                "$..isPrimaryContact": extract(body=body, path='isPrimaryContact')
            })

        return payload

    def calculate_contact_request_type(self, body):
        c_type = extract(body=body, path='$.opportunityContactRequests..contactRequestType.contactRequestTypeId')

        if c_type == OpportunityContactRequestType.NEW.value:
            return OpportunityContactRequestType.NEW.value
        elif c_type == OpportunityContactRequestType.MOD.value:
            return OpportunityContactRequestType.MOD.value
        elif c_type == OpportunityContactRequestType.EXS.value:
            return OpportunityContactRequestType.EXS.value
        else:
            raise ValueError("Contact type %s does not exist. Check test data." % c_type)


class OpportunityContactRequestType(Enum):
    NEW = 1
    MOD = 2
    EXS = 3
