from tools.json_tools import extract
from .case import Case


class CaseRequestJobsite(Case):
    def __init__(self, user):
        super().__init__(user)
        self._user = user

    def get_case_available_jobsites(self, case_request=None, case_request_id=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        url = extract(body=case_request.json(), path='$.links[?(@.rel=="jobsites")].href')
        r = self._user.get(url=url)
        return r

    def patch_case_jobsite(self, case_request=None, case_request_id=None, jobsite_id=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        jobsites = self.get_case_available_jobsites(case_request=case_request)
        if jobsites:
            jobsite_ids = extract(body=jobsites.json(), path='$.jobsites..jobsiteId', multiple=True)
            if jobsite_id in jobsite_ids:
                print('Jobsite available! continue...')
                url = extract(body=jobsites.json(),
                              path='$.jobsites[?(@.jobsiteId==%s)].links[?(@.method=="PATCH")].href' % jobsite_id)
            else:
                print('Choosing the first jobsite available of: %s' % jobsite_ids)
                url = extract(body=jobsites.json(), path='$.jobsites[0].links[?(@.method=="PATCH")].href')

            r = self._user.patch(url=url)
            return r
        else:
            raise ('There are no jobsites available for the chosen case. Check data.')
