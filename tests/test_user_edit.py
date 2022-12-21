from datetime import datetime

import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserEdit(BaseCase):
    def setup(self):
        self.register_url = "https://playground.learnqa.ru/api/user/"
        self.login_url = "https://playground.learnqa.ru/api/user/login"

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_reg_data()
        response1 = requests.post(self.register_url, data=register_data)

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

        response2 = requests.post(self.login_url, data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        edit_url = f"https://playground.learnqa.ru/api/user/{user_id}"
        new_name = "Changed Name"
        response3 = requests.put(edit_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = requests.get(edit_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    def test_edit_without_auth(self):
        # REGISTER
        register_data = self.prepare_reg_data()
        response1 = requests.post(self.register_url, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_name = register_data["firstName"]
        user_id = self.get_json_value(response1, "id")

        # EDIT
        edit_url = f"https://playground.learnqa.ru/api/user/{user_id}"
        new_name = "Changed Name"
        response2 = requests.put(edit_url, data={"firstName": new_name})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "UTF-8") == "Auth token not supplied"

        # GET
        response3 = requests.get(edit_url)
        Assertions.assert_json_value_by_name(response3, "username", first_name, "Wrong name of the user after edit")

    def test_edit_just_created_user_as_another_user(self):
        # REGISTER 1
        register_data = self.prepare_reg_data()
        response1 = requests.post(self.register_url, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_name = register_data["firstName"]
        user_id = self.get_json_value(response1, "id")

        # REGISTER 2
        register_data = self.prepare_reg_data2()
        response2 = requests.post(self.register_url, data=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email1 = register_data["email"]
        password1 = register_data["password"]

        # LOGIN
        login_data = {
            "email": {email1},
            "password": {password1}
        }

        response3 = requests.post(self.login_url, data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # EDIT
        edit_url = f"https://playground.learnqa.ru/api/user/{user_id}"
        new_name = "Changed Name"
        response4 = requests.put(edit_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response4, 200)

        # GET
        response4 = requests.get(edit_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "username", first_name, "Wrong name of the user after edit")

    def test_edit_just_created_user_with_wrong_email(self):
        # REGISTER
        register_data = self.prepare_reg_data()
        response1 = requests.post(self.register_url, data=register_data)

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

        response2 = requests.post(self.login_url, data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        edit_url = f"https://playground.learnqa.ru/api/user/{user_id}"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        new_email = f"lernqa1{random_part}example1.com"
        response3 = requests.put(edit_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                 data={"email": new_email})
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("UTF-8") == "Invalid email format"

        # GET
        response4 = requests.get(edit_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "email", email, "Wrong email of the user after edit")

    def test_edit_just_created_user_with_short_name(self):
        # REGISTER
        register_data = self.prepare_reg_data()
        response1 = requests.post(self.register_url, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = requests.post(self.login_url, data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        edit_url = f"https://playground.learnqa.ru/api/user/{user_id}"
        short_name = "1"
        response3 = requests.put(edit_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                 data={"firstName": short_name})
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("UTF-8") == '{"error":"Too short value for field firstName"}'

        # GET
        response4 = requests.get(edit_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "firstName", first_name,
                                             "Wrong firstName of the user after edit")
