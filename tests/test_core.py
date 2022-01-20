import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import *


class TestLabYak(unittest.TestCase):

    def setUp(self) -> None:
        self.yak1 = LabYak('Betty-1', 4)
        self.yak2 = LabYak('Betty-2', 8)
        self.yak3 = LabYak('Betty-3', 9.5)

    def test_yak_production(self):
        yak1_milk, yak1_skins, yak1_last_age_shaved, yak1_age = self.yak1.yak_production(13)
        yak2_milk, yak2_skins, yak2_last_age_shaved, yak2_age = self.yak2.yak_production(13)
        yak3_milk, yak3_skins, yak3_last_age_shaved, yak3_age = self.yak3.yak_production(13)
        milk_production = yak1_milk + yak2_milk + yak3_milk
        skins_production = yak1_skins + yak2_skins + yak3_skins
        self.assertAlmostEqual(milk_production, 1104.480)
        self.assertEqual(skins_production, 3)
        self.assertEqual(yak1_last_age_shaved, 4.0)
        self.assertEqual(yak2_last_age_shaved, 8.0)
        self.assertEqual(yak3_last_age_shaved, 9.5)
        self.assertEqual(yak1_age, 4.13)
        self.assertEqual(yak2_age, 8.13)
        self.assertEqual(yak3_age, 9.63)

        # result = LabYak('abc', 12)
        # self.assertEqual()
        # with self.assertRaises(ValueError):
        #     result.yak_production()


if __name__ == "__main__":
    unittest.main()