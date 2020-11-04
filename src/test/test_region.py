import unittest

from app.logic_layer.region_ll import RegionLogic
from app.data_layer.models.region_model import RegionModel

class TestRegionLogic(unittest.TestCase):
    def setUp(self):
        self.region = RegionLogic()
        self.region_model_1 = RegionModel(None, 'California', 31000000, 1500000)
        self.region.add(self.region_model_1)

    def tearDown(self):
        self.region.delete(self.region_model_1.id)

    def test_get_regions(self):
        regions = self.region.get_regions()
        self.assertEqual(type(regions), list)
        self.assertEqual(type(regions[0]), dict)

    def test_get_region_by_id(self):
        region = self.region.get_region(self.region_model_1.id)
        self.assertEqual(region["regionID"], str(self.region_model_1.id))
        self.assertEqual(type(region), dict)

    def test_get_region_details(self):
        region_details = self.region.get_region_details(self.region_model_1.id)
        self.assertEqual(region_details, {'population': 31000000, 'registeredVoters': 1500000})

    def test_get_error_region(self):
        election = self.region.get_region(999)
        self.assertEqual(election, None)
        election = self.region.get_region('string')
        self.assertEqual(election, None)


if __name__ == '__main__':
    unittest.main()