import requests

base_url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1- Запрос любого типа без параметра method
response = requests.get(base_url)
print(response.text)
# Выводится - Wrong method provided

# 2 - Запрос HEAD
response = requests.head(base_url)
print(response.text)
print(response.status_code)
# Выводится - в тексте - пусто. Код ответа - 400

# 3 - Запрос с правильным значением method
response = requests.get(base_url, params = {"method": "GET"})
print(response.text)
# Выводится - {"success":"!"}

# 4 - Цикл
list = ["POST", "GET", "PUT", "DELETE"]
for i in list:
    response = requests.get(base_url, params = {f"method": {i}})
    print(f"Запрос GET, метод {i} - ответ {response.text}")
    response = requests.post(base_url, data = {f"method": {i}})
    print(f"Запрос POST, метод {i} - ответ {response.text}")
    response = requests.put(base_url, data = {f"method": {i}})
    print(f"Запрос PUT, метод {i} - ответ {response.text}")
    response = requests.delete(base_url, data = {f"method": {i}})
    print(f"Запрос DELETE, метод {i} - ответ {response.text}")
# Delete принимамет метод GET как все ок

