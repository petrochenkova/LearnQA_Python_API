import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserDelete(BaseCase):
    def test_delete_user_with_id_2(self):
        base_url = "https://playground.learnqa.ru/api/user/2"
        login_url = "https://playground.learnqa.ru/api/user/login"
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        # LOGIN
        response1 = requests.post(login_url, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = requests.delete(base_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("UTF-8") == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'

        # ASSERTING
        base_url = f"https://playground.learnqa.ru/api/user/2"
        response3 = requests.get(base_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 200)
        assert response3.content.decode(
            "UTF-8") == '{"id":"2","username":"Vitaliy","email":"vinkotov@example.com","firstName":"Vitalii","lastName":"Kotov"}'

    def test_delete_just_created_user(self):
        register_url = "https://playground.learnqa.ru/api/user/"
        login_url = "https://playground.learnqa.ru/api/user/login"
        # REGISTER
        register_data = self.prepare_reg_data()
        response1 = requests.post(register_url, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = requests.post(login_url, data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        del_url = f"https://playground.learnqa.ru/api/user/{user_id}"
        response2 = requests.delete(del_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response2, 200)

        # ASSERTING
        response3 = requests.get(del_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 404)
        assert response3.content.decode("UTF-8") == 'User not found'

    def test_delete_another_user(self):
        register_url = "https://playground.learnqa.ru/api/user/"
        login_url = "https://playground.learnqa.ru/api/user/login"
        # REGISTER 1
        register_data = self.prepare_reg_data()
        response1 = requests.post(register_url, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_name = register_data["firstName"]
        user_id = self.get_json_value(response1, "id")

        # REGISTER 2
        register_data = self.prepare_reg_data2()
        response2 = requests.post(register_url, data=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email1 = register_data["email"]
        password1 = register_data["password"]

        # LOGIN
        login_data = {
            "email": {email1},
            "password": {password1}
        }

        response3 = requests.post(login_url, data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # DELETE
        del_url = f"https://playground.learnqa.ru/api/user/{user_id}"
        response4 = requests.delete(del_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 200)

        # ASSERTING
        base_url = f"https://playground.learnqa.ru/api/user/{user_id}"
        response5 = requests.get(base_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response5, 200)
        assert response5.content.decode("UTF-8") == '{"username":"' + first_name + '"}'
