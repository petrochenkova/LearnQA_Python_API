import requests
from datetime import datetime, timedelta

# Запуск - python3 -m pytest -s ex12.py -k "test_cookie"

def test_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    now_time = datetime.now()
    headers_value = response.headers
    current_hour = now_time.hour-3
    if len(str(current_hour)) == 1:
        current_hour = "0"+str(current_hour)
    current_minute = now_time.minute
    if len(str(current_minute)) == 1:
        current_minute = "0" + str(current_minute)
    current_second = now_time.second
    if len(str(current_second)) == 1:
        current_second = "0" + str(current_second)
    server_time = f"{current_hour}:{current_minute}:{current_second}"
    server_datetime = datetime.today().strftime(f"%a, %d %b %Y {server_time} GMT")
    expexted_value = {'Date': f'{server_datetime}', 'Content-Type': 'application/json', 'Content-Length': '15', 'Connection': 'keep-alive', 'Keep-Alive': 'timeout=10', 'Server': 'Apache', 'x-secret-homework-header': 'Some secret value', 'Cache-Control': 'max-age=0', 'Expires': f'{server_datetime}'}
    assert headers_value==expexted_value, f'Полученые headers - {headers_value} не совпадают с ожидаемыми - {expexted_value}'