from pytest import mark

from objects.entities.case_request import CaseRequest
from objects.entities.user import User
from tools.json_tools import pretty_print


@mark.case_request
@mark.parametrize("country", ["MX"])
class CaseRequestsTests:

    @mark.smoke
    def test_case_request_crm(self, app_config, country, load_test_user, load_document_data):
        user_data = load_test_user(user_type='ols', country=country)
        case_file = load_document_data(doc_type='Project')
        u = User(app_config, data=user_data)

        case_request = CaseRequest(u)  # 214 #223

        r = case_request.post_new_case_request(customer_id=u.get_customer_id())
        r = case_request.patch_case_request_description(case_request=r)
        r = case_request.patch_case_request_title(case_request=r)

        pretty_print(r.json())
