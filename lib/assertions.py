from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response:Response, name, expexted_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is jot in JSON format. Response text is {name}"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        assert response_as_dict[name] == expexted_value, error_message
