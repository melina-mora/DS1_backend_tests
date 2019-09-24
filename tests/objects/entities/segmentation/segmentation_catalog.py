from objects.api.config import ConfigSegmentation
from tools.json_tools import *


class SegmentationCatalog:
    def __init__(self, user):
        self._config = ConfigSegmentation().configure_test_data_segmentation()['catalog']
        self._user = user

    def post_segmentation(self):
        pass

    def delete_segmentation(self):
        pass

    def patch_segmentation(self):
        pass

    def get_segmentation(self, code=None, **query):
        apis = self._config['usp_crm_GetSegmentations_v3']
        url = extract(body=apis, path='$.url')
        r = self._user.get(url=url, **query)
        return r
