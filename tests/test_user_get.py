import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase

class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        url = "https://playground.learnqa.ru/api/user/2"
        response = requests.get(url)

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        auth_url = "https://playground.learnqa.ru/api/user/login"
        response1 = requests.post(auth_url, data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        base_url = f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}"
        response2 = requests.get(base_url, headers={"x-csrf-token":token}, cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)


    def test_get_user_details_auth_as_another_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        auth_url = "https://playground.learnqa.ru/api/user/login"
        response1 = requests.post(auth_url, data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        base_url = f"https://playground.learnqa.ru/api/user/1"
        response2 = requests.get(base_url, headers={"x-csrf-token":token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_json_has_key(response2, "username")
        unexpected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response2, unexpected_fields)

