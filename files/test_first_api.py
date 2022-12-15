import requests
import pytest

class TestFirstAPI:
    # Переменная "Список" хранит внутри себя кортежи. Кортежи состоят из парамметров (имена в нашем случае) для запуска тестов.
    names = [
        ("Vitalii"),
        ("Anna"),
        ("")
    ]

    # Первое - имя переменной, в которую pytest будет передавать данные. Второе - переменная, в которой эти данные сейчас хранятся
    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        data = {'name': name}

        response = requests.get(url, params=data)

        assert response.status_code == 200, "Wrong response code"

        response_dict = response.json()
        assert "answer" in response_dict, 'There is no field "answer" in the responce'

        if len(name)==0:
            expected_response_text = "Hello, someone"
        else:
            expected_response_text = f"Hello, {name}"

        actual_response_text = response_dict["answer"]
        assert actual_response_text == expected_response_text, "Actual text in response is not correct"
