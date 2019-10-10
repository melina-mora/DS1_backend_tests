from json import dumps

from requests_toolbelt import MultipartEncoder

from tools.json_tools import extract
from .case import Case


class CaseRequestDocument(Case):
    def __init__(self, user):
        super().__init__(user)
        self._user = user

    def post_case_request_document(self, file, case_request=None, case_request_id=None):
        if case_request_id and case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError("Must specify opportunity or opportunity id to patch document to.")

        url = extract(body=case_request.json(), path='$.links[?(@.rel=="modifycasedocuments")].href')
        filename = 'test_document.pdf'

        mp_encoder = MultipartEncoder(
            fields={
                'documentDetail': dumps({"fileName": filename}),
                'file': (filename, file.open(mode='rb'), 'application/pdf'),
            }
        )

        r = self._user.post(url=url, data=mp_encoder, to_string=True)
        url = extract(body=r.json(), path='$.case.links[?@.rel=="self"].href')
        r = self._user.get(url=url)

        return r
