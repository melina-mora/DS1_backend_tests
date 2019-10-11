from pytest import mark

from objects.entities.segmentation.segmentation_catalog import SegmentationCatalog
from objects.entities.user import User
from tools.json_tools import pretty_print


@mark.segmentation_catalog
@mark.parametrize("country", ["MX"])
class SegmentationCatalogTests:

    @mark.smoke
    def test_segmentation_catalog_is_listed(self, app_config, country, load_test_user):
        user_data = load_test_user(user_type='bso', country=country)
        u = User(app_config, data=user_data)

        cat = SegmentationCatalog(u)
        r = cat.get_segmentation(segmentation_type_id=1)
        pretty_print(r.json())

    def test_segmentation_catalog_full_branch_creation(self, app_config, country, load_test_user):
        user_data = load_test_user(user_type='bso', country=country)
        u = User(app_config, data=user_data)

        cat = SegmentationCatalog(u)
        r = cat.post_segmentation(segmentation_type_code='S')
