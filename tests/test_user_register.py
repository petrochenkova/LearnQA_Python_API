import random
import string
from datetime import datetime

import allure
import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Registration tests")
@allure.feature("Registration")
class TestUserRegister(BaseCase):
    def setup(self):
        self.url = "/user/"

    @allure.title("Successful register user")
    @allure.description("This test successfully register user by prepare data")
    def test_create_user_successfully(self):
        data = self.prepare_reg_data()
        response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Unsuccessful register user with existing email")
    @allure.description("This test doesn't register user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_reg_data(email)
        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        # decode тк ответ приходит с "b'" - не закодирован
        assert response.content.decode(
            "UTF-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.title("Unsuccessful register user with email without '@'")
    @allure.description("This test doesn't register user with email without '@'")
    def test_create_user_with_uncorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_reg_data(email)

        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("UTF-8") == "Invalid email format"

    random_part = datetime.now().strftime("%m%d%Y%H%M%S")
    data = [
        {'username': 'lernqa',
         'firstName': 'lernqa',
         'lastName': 'lernqa',
         'email': f"lernqa{random_part}@example.com"},
        {'password': '123',
         'firstName': 'lernqa',
         'lastName': 'lernqa',
         'email': f"lernqa{random_part}@example.com"},
        {'password': '123',
         'username': 'lernqa',
         'lastName': 'lernqa',
         'email': f"lernqa{random_part}@example.com"},
        {'password': '123',
         'username': 'lernqa',
         'firstName': 'lernqa',
         'email': f"lernqa{random_part}@example.com"},
        {'password': '123',
         'username': 'lernqa',
         'firstName': 'lernqa',
         'lastName': 'lernqa'}
    ]

    @allure.title("Unsuccessful register user with missed param")
    @allure.description("This test doesn't register user with missed param")
    @pytest.mark.parametrize('data', data)
    def test_create_user_without_one_field(self, data):
        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        if "password" not in data:
            assert response.content.decode("UTF-8") == "The following required params are missed: password"
        elif "username" not in data:
            assert response.content.decode("UTF-8") == "The following required params are missed: username"
        elif "firstName" not in data:
            assert response.content.decode("UTF-8") == "The following required params are missed: firstName"
        elif "lastName" not in data:
            assert response.content.decode("UTF-8") == "The following required params are missed: lastName"
        elif "email" not in data:
            assert response.content.decode("UTF-8") == "The following required params are missed: email"

    @allure.title("Unsuccessful register user with too short name")
    @allure.description("This test doesn't register user with too short name")
    def test_create_user_with_short_name(self):
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        data = {
            'password': '123',
            'username': 'l',
            'firstName': 'lernqa',
            'lastName': 'lernqa',
            'email': f"lernqa{random_part}@example.com"
        }
        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("UTF-8") == "The value of 'username' field is too short"

    @allure.title("Unsuccessful register user too long name")
    @allure.description("This test doesn't register user with too long name")
    def test_create_user_with_long_name(self):
        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(251))
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        data = {
            'password': '123',
            'username': name,
            'firstName': 'lernqa',
            'lastName': 'lernqa',
            'email': f"lernqa{random_part}@example.com"
        }
        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("UTF-8") == "The value of 'username' field is too long"
