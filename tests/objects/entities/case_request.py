from .case.case_request_businesslines import CaseRequestBusinessLines
from .case.case_request_contact import CaseRequestContact
from .case.case_request_documents import CaseRequestDocument
from .case.case_request_jobsite import CaseRequestJobsite


class CaseRequest(CaseRequestJobsite, CaseRequestContact, CaseRequestBusinessLines, CaseRequestDocument):
    def __init__(self, user):
        super().__init__(user)
