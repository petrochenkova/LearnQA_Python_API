import time
import requests

base_url = "https://playground.learnqa.ru/ajax/api/longtime_job"
# 1 - Создание задачи
response = requests.get(base_url)
seconds = response.json()["seconds"]
token = response.json()["token"]
# 2 - Один запрос с token ДО
response = requests.get(base_url, params={f"token":{token}})
assert response.json()["status"] == "Job is NOT ready"
# 3 - Ожидание
time.sleep(seconds)
# 4 - Один запрос c token ПОСЛЕ
response = requests.get(base_url, params={f"token":{token}})
assert response.json()["status"] == "Job is ready" and "result" in response.json()


