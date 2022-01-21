import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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

    def test_get_herd_info_extreme_cases(self):
        # day 0 test
        with self.assertRaises(ValueError) as e:
            self.app.get('/yak-shop/herd/0')
        the_exception = str(e.exception)
        self.assertEqual(the_exception, "Days should start with 1 and could not be a float number.")

        # a randomly large day
        response = self.app.get('/yak-shop/herd/10000')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertEqual(content["herd"][0].get("age"), 10.0)
        self.assertEqual(content["herd"][1].get("age"), 10.0)
        self.assertEqual(content["herd"][2].get("age"), 10.0)
        self.assertEqual(content["herd"][0].get("age-last-shaved"), 9.82)
        self.assertEqual(content["herd"][1].get("age-last-shaved"), 9.93)
        self.assertEqual(content["herd"][2].get("age-last-shaved"), 9.86)

    def test_get_herd_info_normal_cases(self):
        # day 13 test
        response = self.app.get('/yak-shop/herd/13')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertEqual(content["herd"][0].get("age"), 4.13)
        self.assertEqual(content["herd"][1].get("age"), 8.13)
        self.assertEqual(content["herd"][2].get("age"), 9.63)
        self.assertEqual(content["herd"][0].get("age-last-shaved"), 4.0)
        self.assertEqual(content["herd"][1].get("age-last-shaved"), 8.0)
        self.assertEqual(content["herd"][2].get("age-last-shaved"), 9.5)

        # day 14 test
        response = self.app.get('/yak-shop/herd/14')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertEqual(content["herd"][0].get("age"), 4.14)
        self.assertEqual(content["herd"][1].get("age"), 8.14)
        self.assertEqual(content["herd"][2].get("age"), 9.64)
        self.assertEqual(content["herd"][0].get("age-last-shaved"), 4.13)
        self.assertEqual(content["herd"][1].get("age-last-shaved"), 8.0)
        self.assertEqual(content["herd"][2].get("age-last-shaved"), 9.5)

        # day 18 test
        response = self.app.get('/yak-shop/herd/18')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertEqual(content["herd"][0].get("age"), 4.18)
        self.assertEqual(content["herd"][1].get("age"), 8.18)
        self.assertEqual(content["herd"][2].get("age"), 9.68)
        self.assertEqual(content["herd"][0].get("age-last-shaved"), 4.13)
        self.assertEqual(content["herd"][1].get("age-last-shaved"), 8.17)
        self.assertEqual(content["herd"][2].get("age-last-shaved"), 9.5)

        # day 19 test
        response = self.app.get('/yak-shop/herd/19')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertEqual(content["herd"][0].get("age"), 4.19)
        self.assertEqual(content["herd"][1].get("age"), 8.19)
        self.assertEqual(content["herd"][2].get("age"), 9.69)
        self.assertEqual(content["herd"][0].get("age-last-shaved"), 4.13)
        self.assertEqual(content["herd"][1].get("age-last-shaved"), 8.17)
        self.assertEqual(content["herd"][2].get("age-last-shaved"), 9.68)

    def test_get_stock_info_extreme_cases(self):
        # day 0 test
        with self.assertRaises(ValueError) as e:
            self.app.get('/yak-shop/herd/0')
        the_exception = str(e.exception)
        self.assertEqual(the_exception, "Days should start with 1 and could not be a float number.")

        # a randomly large day
        response = self.app.get('/yak-shop/stock/10000')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertAlmostEqual(content.get("milk"), 23050.25)
        self.assertEqual(content.get("skins"), 54)

    def test_get_stock_info_normal_cases(self):
        # day 13 test
        response = self.app.get('/yak-shop/stock/13')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertAlmostEqual(content.get("milk"), 1104.48)
        self.assertEqual(content.get("skins"), 3)

        # day 14 test
        response = self.app.get('/yak-shop/stock/14')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertAlmostEqual(content.get("milk"), 1188.81)
        self.assertEqual(content.get("skins"), 4)

        # day 18 test
        response = self.app.get('/yak-shop/stock/18')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertAlmostEqual(content.get("milk"), 1525.23)
        self.assertEqual(content.get("skins"), 5)

        # day 19 test
        response = self.app.get('/yak-shop/stock/19')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertAlmostEqual(content.get("milk"), 1609.11)
        self.assertEqual(content.get("skins"), 6)

    def test_create_order(self):
        # test for 201 condition
        response = self.app.post('/yak-shop/order/13', json={
            "customer": "Medvedev1",
            "order": {"milk": 1000, "skins": 1}
        })
        status_code = response.status_code
        self.assertEqual(status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertAlmostEqual(content[1].get("milk"), 1000.0)
        self.assertEqual(content[1].get("skins"), 1)

        # test for 206 condition
        response = self.app.post('/yak-shop/order/13', json={
            "customer": "Medvedev2",
            "order": {"milk": 1000, "skins": 1}
        })
        status_code = response.status_code
        self.assertEqual(status_code, 206)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertEqual(content[1].get("milk"), None)
        self.assertEqual(content[1].get("skins"), 1)

        # test for 206 condition
        response = self.app.post('/yak-shop/order/13', json={
            "customer": "Medvedev3",
            "order": {"milk": 100, "skins": 2}
        })
        status_code = response.status_code
        self.assertEqual(status_code, 206)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertAlmostEqual(content[1].get("milk"), 100.0)
        self.assertEqual(content[1].get("skins"), None)

        # test for 404 condition
        response = self.app.post('/yak-shop/order/13', json={
            "customer": "Medvedev4",
            "order": {"milk": 100, "skins": 2}
        })
        status_code = response.status_code
        self.assertEqual(status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertEqual(content[0].get("milk"), None)
        self.assertEqual(content[0].get("skins"), None)

        # test for the same order but next day
        response = self.app.post('/yak-shop/order/14', json={
            "customer": "Medvedev5",
            "order": {"milk": 100, "skins": 2}
        })
        status_code = response.status_code
        self.assertEqual(status_code, 206)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertEqual(content[1].get("milk"), None)
        self.assertEqual(content[1].get("skins"), 2)

        # test for descending order of time
        response = self.app.post('/yak-shop/order/13', json={
            "customer": "Medvedev6",
            "order": {"milk": 100, "skins": 2}
        })
        status_code = response.status_code
        self.assertEqual(status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        content = response.get_json()
        self.assertTrue(content.get("error message"))


if __name__ == "__main__":
    unittest.main()