from pytest import mark

from objects.entities.case_request import CaseRequest
from objects.entities.user import User
from tools.json_tools import pretty_print


@mark.case_request
class CaseRequestsTests:

    @mark.smoke
    @mark.parametrize("country", ["MX"])
    def test_case_request(self, app_config, country, load_test_user, load_document_data):
        user_data = load_test_user(user_type='crm', country=country, legal_entity_id='160413.1')
        file = load_document_data()
        u = User(app_config, data=user_data)

        case_request = CaseRequest(u)

        r = case_request.post_new_case_request(customer_id=u.get_customer_id())
        r = case_request.patch_case_request_description(case_request=r)
        r = case_request.patch_case_request_title(case_request=r)
        r = case_request.patch_case_request_type(case_request=r)
        r = case_request.patch_case_jobsite(case_request=r, jobsite_id=394932)
        r = case_request.put_case_businesslines(case_request=r, businessline_id=2)
        r = case_request.put_case_contact(case_request=r, contact_id=258107)
        r = case_request.post_case_request_document(case_request=r, file=file)
        r = case_request.patch_case_to_requested(case_request=r)

        pretty_print(r.json())
