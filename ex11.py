import requests

# Запуск - python3 -m pytest -s ex11.py -k "test_cookie"
def test_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    actual_cookie_value = response.cookies.get("HomeWork")
    assert actual_cookie_value != None, f'Cookie не пришло'