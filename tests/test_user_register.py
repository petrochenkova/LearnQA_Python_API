import random
import string
from datetime import datetime

import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    def setup(self):
        self.url = "/user/"

    def test_create_user_successfully(self):
        data = self.prepare_reg_data()
        response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_reg_data(email)
        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        # decode тк ответ приходит с "b'" - не закодирован
        assert response.content.decode(
            "UTF-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

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
