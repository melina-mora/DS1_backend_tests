from scripts.mongo_tools_script.mongo_connection import MongoDBConnection
from tools.exceptions import DataError
from tools.json_tools import update_json, extract


class CaseRequest:
    def __init__(self, user):
        self._user = user

        self._case_request_type = None
        self._case_request_id = None

        self._db = MongoDBConnection(db='TestData', coll='JsonModels')

    def get_case_request_by_id(self, case_request_id):
        json = self._db.coll.find_one({'json_model': 'new_case_request'}, {'url': 1, '_id': 0})
        url = ''.join([json, case_request_id])
        case_request = self._user.get(url=url)
        return case_request

    def post_new_case_request(self, customer_id=None, payload=None):
        json = self._db.coll.find_one({'json_model': 'new_case_request'}, {'payload': 1, 'url': 1, '_id': 0})
        url = extract(body=json, path='$.url')

        if not payload and customer_id:
            payload = update_json(body=json['payload'], values={'$..customerId': customer_id})

        r = self._user.post(url=url, payload=payload)
        return r

    def patch_case_request_description(self, case_request=None, case_request_id=None, payload=None):
        if not case_request and case_request_id:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        url = extract(body=case_request.json(), path="$.links[?(@.rel=='modifydescription')].href")

        json = self._db.coll.find_one({'json_model': 'modify_case_request_description'},
                                      {'payload': 1, '_id': 0})
        if not payload:
            payload = extract(body=json, path='$.payload')

        r = self._user.patch(url=url, payload=payload)
        return r

    def patch_case_request_title(self, case_request=None, case_request_id=None, payload=None):
        if not case_request and case_request_id:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        url = extract(body=case_request.json(), path="$.links[?(@.rel=='modifytitle')].href")

        json = self._db.coll.find_one({'json_model': 'modify_case_request_title'},
                                      {'payload': 1, '_id': 0})
        if not payload:
            payload = extract(body=json, path='$.payload')

        r = self._user.patch(url=url, payload=payload)
        return r

    def patch_case_request_title(self, case_request=None, case_request_id=None, payload=None):
        if not case_request and case_request_id:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        url = extract(body=case_request.json(), path="$.links[?(@.rel=='modifytitle')].href")

        json = self._db.coll.find_one({'json_model': 'modify_case_request_title'},
                                      {'payload': 1, '_id': 0})
        if not payload:
            payload = extract(body=json, path='$.payload')

        r = self._user.patch(url=url, payload=payload)
        return r

    def get_case_types(self, case_request_id=None, case_request=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        url = extract(body=case_request.json(), path="$.links[?(@.rel=='casetypes')].href")

        types = self._user.get(url=url)
        return types

    def patch_case_request_type(self, case_request_id=None, case_request=None, case_type_id=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        types = self.get_case_types(case_request=case_request)

        if case_type_id:
            type_ids = extract(body=types.json(), path='$.caseTypes.caseTypeId', multiple=True)
            if type_ids:
                if case_type_id not in type_ids:
                    print('CaseTypeId: %s not available for this case, choosing first available of %s' % type_ids)
                    url = extract(body=types.json(), path="$.caseTypes[?@.caseTypeId=%s].links[?@.method='PATCH']")
                else:
                    print('CaseTypeId available! continue')
                    url = extract(body=types.json(), path='$.caseTypes.caseTypeId', multiple=True)
            elif not type_ids:
                raise DataError('There are no case types available for the chosen case. Check data.')

            r = self._user.patch(url=url)
            return r
