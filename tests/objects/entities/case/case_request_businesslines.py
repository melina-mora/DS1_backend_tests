from scripts.mongo_tools_script.mongo_connection import MongoDBConnection
from tools.json_tools import update_json, extract
from .case import Case


class CaseRequestBusinessLines(Case):
    def __init__(self, user):
        super().__init__(user)
        self._user = user

    def get_case_available_businesslines(self, case_request=None, case_request_id=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        url = extract(body=case_request.json(), path='$.links[?(@.rel=="businesslines")].href')
        r = self._user.get(url=url)
        return r

    def put_case_businesslines(self, case_request=None, case_request_id=None, businessline_id=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        url = extract(body=case_request.json(), path='$.links[?(@.rel=="modifycasebusinesslines")].href')
        payload = self.set_valid_business_line_to_patch(case_request=case_request, businessline_id=businessline_id)

        r = self._user.put(url=url, payload=payload)
        url = extract(body=r.json(), path='$.caseBusinessLines..case.links[?(@.rel=="self")].href')
        r = self._user.get(url=url)
        return r

    def set_valid_business_line_to_patch(self, case_request=None, case_request_id=None, businessline_id=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        businesslines = self.get_case_available_businesslines(case_request=case_request)

        if businesslines:
            bls_ids = extract(body=businesslines.json(), path='$.businessLines..businessLineId', multiple=True)
            if businessline_id and businessline_id in bls_ids and isinstance(businessline_id, int):
                print('BusinessLine available! continue...')
                return self.prepare_case_business_line_payload(businessline_id=businessline_id)
            else:
                print('Choosing the first businessline available of: %s' % bls_ids)
                return self.prepare_case_business_line_payload(businessline_id=bls_ids[0])
        else:
            raise ('There are no businessLines available for the chosen case. Check data.')

    def prepare_case_business_line_payload(self, businessline_id):
        payload = MongoDBConnection(db='TestData', coll='JsonModels')
        payload = payload.coll.find_one({'json_model': 'modify_case_businesslines'}, {'payload': 1, '_id': 0})[
            'payload']
        payload = update_json(body=payload,
                              values={'$.caseBusinessLines..businessLine.businessLineId': businessline_id})
        return payload
