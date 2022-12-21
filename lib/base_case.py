import json.decoder
from datetime import datetime

from requests import Response

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f'Cannot find cookie with name {cookie_name} in the last responce'
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f'Cannot find header with name {headers_name} in the last responce'
        return response.headers[headers_name]

    def get_json_value(self, response:Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def prepare_reg_data(self, email=None):
        if email is None:
            base_part = "lernqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'lernqa',
            'firstName': 'lernqa',
            'lastName': 'lernqa',
            'email': email
        }

    def prepare_reg_data2(self, email=None):
        if email is None:
            base_part = "lernqa1"
            domain = "example1.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'lernqa1',
            'firstName': 'lernqa1',
            'lastName': 'lernqa1',
            'email': email
        }
