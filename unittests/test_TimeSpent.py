import unittest
from Configuration.rush import Rush
import ShopperModel.shopper

class TestTimeSpent(unittest.TestCase):
    def test_time_spent(self):
        expected_avg_time = 15
        rush = Rush("1400", "1500", 20, 0.2, 6, 75, 15)
        self.assertEqual(expected_avg_time, rush.normal_avg_time)
