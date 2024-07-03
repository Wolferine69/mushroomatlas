# Create your tests here.
# Create your tests here.
import unittest
import requests


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"
        self.login_url = f"{self.base_url}/api/token/"
        self.username = "FungiFreak"
        self.password = "FunGuy123!"
        self.client = requests.Session()
        self.token = self.get_token()
        self.headers = {
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json'
        }

    def get_token(self):
        login_data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.login_url, json=login_data)

        self.assertEqual(response.status_code, 200)

        try:
            json_response = response.json()
        except ValueError:
            self.fail(f"Response is not valid JSON: {response.text}")

        token = json_response.get("token")
        if not token:
            self.fail(f"No token found in response: {response.text}")

        return token

    def test_get_mushrooms(self):
        response = self.client.get(f"{self.base_url}/api/mushrooms/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_post_mushroom(self):
        habitats_response = self.client.get(f"{self.base_url}/api/habitats/", headers=self.headers)
        self.assertEqual(habitats_response.status_code, 200)
        habitats_data = habitats_response.json()
        if not habitats_data:
            self.fail("No habitats found")

        habitat_id = habitats_data[0]['id']

        payload = {
            "name_cz": "Testovací houba",
            "name_latin": "Testus fungus",
            "description": "A test mushroom for unit tests",
            "edibility": "jedla",
            "habitats": [habitat_id],
            "image": None,
            "family": None
        }

        response = self.client.post(f"{self.base_url}/api/mushrooms/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("name_cz", response.json())
        self.assertEqual(response.json()["name_cz"], "Testovací houba")


if __name__ == '__main__':
    unittest.main()

