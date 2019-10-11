from scripts.mongo_tools_script.mongo_connection import MongoDBConnection
from tools.json_tools import update_json, extract
from .case import Case


class CaseRequestContact(Case):
    def __init__(self, user):
        super().__init__(user)
        self._user = user

    def get_case_available_contacts(self, case_request=None, case_request_id=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        url = extract(body=case_request.json(), path='$.links[?(@.rel=="contacts")].href')
        r = self._user.get(url=url)
        return r

    def put_case_contact(self, case_request=None, case_request_id=None, contact_id=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        url = extract(body=case_request.json(), path='$.links[?(@.rel=="modifycasecontacts")].href')
        payload = self.set_valid_contact_to_patch(case_request=case_request, contact_id=contact_id)

        r = self._user.put(url=url, payload=payload)
        url = extract(body=r.json(), path='$.caseContacts..case.links[?(@.rel=="self")].href')
        r = self._user.get(url=url)
        return r

    def set_valid_contact_to_patch(self, case_request=None, case_request_id=None, contact_id=None):
        if case_request_id and not case_request:
            case_request = self.get_case_request_by_id(case_request_id=case_request_id)
        elif not case_request:
            raise ValueError('Must specify case object or case id to patch description.')

        contacts = self.get_case_available_contacts(case_request=case_request)

        contacts_ids = extract(body=contacts.json(), path='$.contacts..contactId', multiple=True)
        if contact_id and contact_id in contacts and isinstance(contact_id, int):
            print('ContactId available! continue...')
            return self.prepare_contact_payload(contact_id=contact_id)
        else:
            try:
                print('Choosing the first contact available of: %s' % contacts_ids)
                return self.prepare_contact_payload(contact_id=contacts_ids[0])
            except IndexError as e:
                raise ('There are no contacts available for the chosen case. Check data.')


    def prepare_contact_payload(self, contact_id):
        payload = MongoDBConnection(db='TestData', coll='JsonModels')
        payload = payload.coll.find_one({'json_model': 'modify_case_contacts'}, {'payload': 1, '_id': 0})['payload']
        payload = update_json(body=payload,
                              values={'$.caseContacts..contact.contactId': contact_id})
        return payload
