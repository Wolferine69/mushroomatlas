import unittest
import requests

class TestAPI(unittest.TestCase):

    def setUp(self):
        # Base URL of the API
        self.base_url = "http://127.0.0.1:8000"
        # URL for obtaining the authentication token
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
        # Obtain the authentication token
        login_data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.login_url, json=login_data)
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        token = json_response.get("token")
        self.assertIsNotNone(token, f"No token found in response: {response.text}")
        return token

    def test_get_mushrooms(self):
        # Test for fetching the list of mushrooms
        response = self.client.get(f"{self.base_url}/api/mushrooms/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_post_mushroom(self):
        # Test for creating a new mushroom entry
        habitats_response = self.client.get(f"{self.base_url}/api/habitats/", headers=self.headers)
        self.assertEqual(habitats_response.status_code, 200)
        habitats_data = habitats_response.json()
        self.assertTrue(habitats_data, "No habitats found")
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
        self.assertEqual(response.json()["name_cz"], "Testovací houba")

    def test_get_families(self):
        # Test for fetching the list of families
        response = self.client.get(f"{self.base_url}/api/families/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_post_family(self):
        # Test for creating a new family entry
        payload = {
            "name": "Testovací rodina",
            "name_latin": "Familia testus",
            "description": "A test family for unit tests"
        }
        response = self.client.post(f"{self.base_url}/api/families/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Testovací rodina")

    def test_get_recipes(self):
        # Test for fetching the list of recipes
        response = self.client.get(f"{self.base_url}/api/recipes/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_post_recipe(self):
        # Test for creating a new recipe entry
        profile_id = self.get_profile_id(user_id=1)
        payload = {
            "user": profile_id,
            "title": "Testovací recept",
            "ingredients": "Ingredience test",
            "instructions": "Instrukce test",
            "image": None,
            "main_mushroom": None,
            "source": "Test source"
        }
        response = self.client.post(f"{self.base_url}/api/recipes/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Testovací recept")

    def get_profile_id(self, user_id):
        # Helper function to fetch the profile ID for a given user ID
        response = self.client.get(f"{self.base_url}/api/profiles/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        profiles = response.json()
        profile = next((p for p in profiles if p['user'] == user_id), None)
        self.assertIsNotNone(profile, f"No profile found for user ID {user_id}")
        return profile['id']

    def test_get_findings(self):
        # Test for fetching the list of findings
        response = self.client.get(f"{self.base_url}/api/findings/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_post_finding(self):
        # Test for creating a new finding entry
        mushrooms_response = self.client.get(f"{self.base_url}/api/mushrooms/", headers=self.headers)
        self.assertEqual(mushrooms_response.status_code, 200)
        mushrooms_data = mushrooms_response.json()
        self.assertTrue(mushrooms_data, "No mushrooms found")
        mushroom_id = mushrooms_data[0]['id']
        profile_id = self.get_profile_id(user_id=1)
        payload = {
            "user": profile_id,
            "mushroom": mushroom_id,
            "description": "Test finding description",
            "date_found": "2024-07-04",
            "latitude": 50.0755,
            "longitude": 14.4378,
            "image": None
        }
        response = self.client.post(f"{self.base_url}/api/findings/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["description"], "Test finding description")

    def test_get_habitats(self):
        # Test for fetching the list of habitats
        response = self.client.get(f"{self.base_url}/api/habitats/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_post_habitat(self):
        # Test for creating a new habitat entry
        payload = {
            "name": "Testovací habitat"
        }
        response = self.client.post(f"{self.base_url}/api/habitats/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Testovací habitat")

if __name__ == '__main__':
    unittest.main()
