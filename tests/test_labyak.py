import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import LabYak


class TestLabYak(unittest.TestCase):

    def test_instance_creation(self):
        # test for age > 10
        with self.assertRaises(AssertionError) as e:
            yak1 = LabYak('Betty-4', 11)
        the_exception = str(e.exception)
        self.assertEqual(the_exception, "Invalid age! The initial age must be between 0 and 10!")
        # test for age < 0
        with self.assertRaises(AssertionError) as e:
            yak2 = LabYak('Betty-4', -1)
        the_exception = str(e.exception)
        self.assertEqual(the_exception, "Invalid age! The initial age must be between 0 and 10!")

    def test_set_readonly_attribute(self):
        yak1 = LabYak('Betty-1', 4)
        with self.assertRaises(AttributeError) as e:
            yak1.age = 5
        the_exception = str(e.exception)
        self.assertEqual(the_exception, "Yak age is read-only")

    def test_yak_production(self):
        yak1 = LabYak('Betty-1', 4)
        # test for a negative day
        with self.assertRaises(ValueError) as e:
            yak1.yak_production(-1)
        the_exception = str(e.exception)
        self.assertEqual(the_exception, "Days should start with 1 and could not be a float number.")
        # test for a float day
        with self.assertRaises(ValueError) as e:
            yak1.yak_production(2.5)
        the_exception = str(e.exception)
        self.assertEqual(the_exception, "Days should start with 1 and could not be a float number.")

    def test_wool_production(self):
        # test for an adult yak
        yak1 = LabYak('Betty-1', 5)
        yak1._wool_production(3)
        self.assertEqual(yak1.wool_production, 1)
        self.assertEqual(yak1.age_last_shaved, 5)
        # test for a baby yak
        yak2 = LabYak('Betty-2', 0.5)
        yak2._wool_production(3)
        self.assertEqual(yak2.wool_production, 0)
        self.assertEqual(yak2.age_last_shaved, None)
        yak2._wool_production(51)
        self.assertEqual(yak2.age_last_shaved, 1)
        self.assertEqual(yak2.wool_production, 1)


if __name__ == "__main__":
    unittest.main()