from data.db.db_connection import MongoDBConnection
from tools.json_tools import *
from tools.validators.validate_roles import roles


class SegmentationCatalog:
    def __init__(self, user):
        self._db = MongoDBConnection(db='TestData', coll='JsonModels')
        self._user = user

    @roles('SEGCAT_EDIT', 'SEGCAT_VIEW')
    def post_segmentation(self, segmentation_type_code=None, payload=None):
        json_model = self._db.coll.find_one({'json_model': 'post_segmentation'},
                                            {"url": 1, "payload": 1, "_id": 0})

        if not payload and segmentation_type_code:
            payload = extract(body=json_model, path='$.payload')
            payload = update_json(body=payload, values={'$.segmentationCode': segmentation_type_code})
        elif not (segmentation_type_code and payload):
            raise ('Must specify segmentationTypeCode to create. Check script or payload provided.')

        url = extract(body=json_model, path='$.url')

        r = self._user.post(url=url, payload=payload)
        return r

    def delete_segmentation(self):
        pass

    def patch_segmentation(self):
        pass

    def get_segmentation(self, **query):
        apis = self._db.coll.find_one({'json_model': 'get_segmentation'},
                                      {"url": 1, "payload": 1, "_id": 0})
        url = extract(body=apis, path='$.url')
        r = self._user.get(url=url, **query)
        return r
