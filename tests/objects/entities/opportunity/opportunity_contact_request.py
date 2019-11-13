from enum import Enum

from objects.entities.opportunity.opportunity import Opportunity
from tools.json_tools import *


class OpportunityContactRequest(Opportunity):

    def __init__(self, user, code):
        super().__init__(user, code)
        self._user = user
        self._code = code
        self._config = super().set_opp_config()
        self._catalogs = super().set_opp_catalogs()

    def put_opportunity_contact_request(self, opportunity=None, opportunity_id=None, payload=None):
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
        if payload:
            payload = payload
        else:
            payload = self.fetch_db(coll='JsonModels')
            payload = payload.coll.find_one({'json_model': 'contact'}, {'payload': 1, '_id': 0})['payload']
            payload = self.set_contact_request_data(body=payload)

        r = self._user.put(url=url, payload=payload)
        opp_id = extract(body=r.json(), path='$.opportunityContactRequests..opportunity.opportunityId')
        r = self.get_opportunity_by_id(opportunity_id=opp_id)
        return r

    def set_contact_request_data(self, body=None):
        if body is None:
            raise ValueError("Must specify data for contact, check test data. Body:\n %s \n" % body)
        else:
            contact_type = self.calculate_contact_request_type(body=body)
            contact_country = self._user.country
            contact_role = self.calculate_contact_request_role(country=contact_country)

            payload = update_json(body=body, values={
                "$..contactRequest.countryAreaCode": contact_country,
                "$..contactRequest.contactRequestType.contactRequestTypeId": contact_type,
                "$..contactRole.contactPersonRoleId": contact_role,
                "$..contactPersonRole.contactPersonRoleId": contact_role
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

    def calculate_contact_request_role(self, country):
        apis = self._catalogs.get('usp_im_GetContactPersonRoles_Catalog_v2')
        url = apis.get('url')
        r = self._user.get(url=url, country_code=country)

        roles = extract(body=r.json(), path='$.contactPersonRoles..contactPersonRoleId', multiple=True)
        if isinstance(roles, list) and len(roles) > 0:
            return roles[0]
        else:
            raise DataError('Could not find any role available for specified country.')


class OpportunityContactRequestType(Enum):
    NEW = 1
    MOD = 2
    EXS = 3
