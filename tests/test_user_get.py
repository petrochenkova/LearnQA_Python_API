import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Get user info tests")
@allure.feature("Get user info")
class TestUserGet(BaseCase):

    @allure.title("Get user details without authorization")
    @allure.description("This test get only username without authorization")
    def test_get_user_details_not_auth(self):
        url = "/user/2"
        response = MyRequests.get(url)

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.title("Get user details with authorization")
    @allure.description("This test get all fields with authorization")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        auth_url = "/user/login"
        response1 = MyRequests.post(auth_url, data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        base_url = f"/user/{user_id_from_auth_method}"
        response2 = MyRequests.get(base_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title("Get user details with authorization as different user")
    @allure.description("This test get only username with authorization as different user")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        auth_url = "/user/login"
        response1 = MyRequests.post(auth_url, data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        base_url = f"/user/1"
        response2 = MyRequests.get(base_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_json_has_key(response2, "username")
        unexpected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response2, unexpected_fields)
