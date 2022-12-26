import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserAuth(BaseCase):
    # Переменная "Список" хранит внутри себя кортежи. Кортежи состоят из парамметров для запуска тестов.
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_auth_user(self):
        response2 = MyRequests.get("/user/auth", headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2, "user_id", self.user_id_from_auth_method,
                                             "User id from auth method is not equal to user id from check method")

    # Первое - имя переменной, в которую pytest будет передавать данные. Второе - переменная, в которой эти данные сейчас хранятся
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = MyRequests.get("/user/auth", headers={"x-csrf-token": self.token})
        else:
            response2 = MyRequests.get("/user/auth", cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2, "user_id", 0,
                                             "User is authorized with condition {condition}")
