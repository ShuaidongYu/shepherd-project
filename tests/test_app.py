import unittest
import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
    
    def test_get_yak_shop(self):
        response = self.app.get('/yak-shop')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_stock(self):
        response = self.app.get('/yak-shop/stock')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_herd(self):
        response = self.app.get('/yak-shop/herd')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_herd_info(self):
        result = self.app.get('/yak-shop/herd/13')
        status_code = result.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(result.content_type, "application/json")
        content = result.get_json()
        self.assertEqual(content["herd"][0].get("age"), 4.13)
        self.assertEqual(content["herd"][1].get("age"), 8.13)
        self.assertEqual(content["herd"][2].get("age"), 9.63)
        self.assertEqual(content["herd"][0].get("age-last-shaved"), 4.0)
        self.assertEqual(content["herd"][1].get("age-last-shaved"), 8.0)
        self.assertEqual(content["herd"][2].get("age-last-shaved"), 9.5)

        result = self.app.get('/yak-shop/herd/14')
        status_code = result.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(result.content_type, "application/json")
        content = result.get_json()
        self.assertEqual(content["herd"][0].get("age"), 4.14)
        self.assertEqual(content["herd"][1].get("age"), 8.14)
        self.assertEqual(content["herd"][2].get("age"), 9.64)
        self.assertEqual(content["herd"][0].get("age-last-shaved"), 4.13)
        self.assertEqual(content["herd"][1].get("age-last-shaved"), 8.0)
        self.assertEqual(content["herd"][2].get("age-last-shaved"), 9.5)

    def test_get_stock_info(self):
        result = self.app.get('/yak-shop/stock/13')
        status_code = result.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(result.content_type, "application/json")
        content = result.get_json()
        self.assertAlmostEqual(content.get("milk"), 1104.48)
        self.assertEqual(content.get("skins"), 3)

        result = self.app.get('/yak-shop/stock/14')
        status_code = result.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(result.content_type, "application/json")
        content = result.get_json()
        self.assertAlmostEqual(content.get("milk"), 1188.81)
        self.assertEqual(content.get("skins"), 4)


if __name__ == "__main__":
    unittest.main()