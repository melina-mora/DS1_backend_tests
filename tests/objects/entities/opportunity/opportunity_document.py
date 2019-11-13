from datetime import datetime

from requests_toolbelt.multipart.encoder import MultipartEncoder

from objects.entities.opportunity.opportunity import Opportunity
from tools.json_tools import *


class OpportunityDocument(Opportunity):

    def __init__(self, user, code):
        super().__init__(user, code)
        self._user = user
        self._code = code
        self._config = super().set_opp_config()

    def patch_opportunity_document(self, opportunity, opportunity_id, document_type, file):
        if opportunity_id and not opportunity:
            opportunity = self.get_opportunity_by_id(opportunity_id=opportunity_id)
        elif not opportunity:
            raise ValueError("Must specify opportunity or opportunity id to patch document to.")

        body = opportunity.json()

        if document_type == "Project":
            url = extract(body=body, path='$.links.addProjectDocument')
            filename = 'project.pdf'
        else:
            url = extract(body=body, path='$.links.addTaxableDocument')
            filename = 'test_document.pdf'

        mp_encoder = MultipartEncoder(
            fields={
                'file': (filename, file.open(mode='rb+'), 'application/pdf'),
            }
        )

        r = self._user.post(url=url, data=mp_encoder)

        return r

    def patch_opportunity_document_dates_and_comment(self, opportunity, opportunity_id, test_data=None):
        if opportunity_id and not opportunity:
            opportunity = self.get_opportunity_by_id(opportunity_id=opportunity_id)
        elif not opportunity:
            raise ValueError("Must specify opportunity or opportunity id to patch document to.")

        if not test_data:
            conn = self.fetch_db(db='TestData', coll='JsonModels')
            body = conn.coll.find_one({'json_model':'project'}, {'payload':1, '_id':0})
            body = update_json(body=body.get('payload'), values={
                '$.project.projectFrom': datetime.now().strftime('%Y-%m-%dT23:00:00.000Z'),
                '$.project.projectTo': '2022-09-02T22:00:00.000Z'
            })
        elif isinstance(test_data, dict):
            body = test_data
        else:
            raise DataError('Must specify test data in JSON format.')

        url = extract(body=opportunity.json(), path='$.links.self')
        r = self._user.patch(url=url, payload=body)
        return r
