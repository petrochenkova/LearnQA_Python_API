import requests

# response = requests.get("https://playground.learnqa.ru/api/check_type", params = {"param1": "value1"})
# print(response.text)

# response = requests.post("https://playground.learnqa.ru/api/check_type", data = {"param1": "value1"})
# print(response.text)

# response = requests.delete("https://playground.learnqa.ru/api/check_type", data = {"param1": "value1"})
# print(response.text)

# response = requests.put("https://playground.learnqa.ru/api/check_type", data = {"param1": "value1"})
# print(response.text)

# 200
# response = requests.post("https://playground.learnqa.ru/api/check_type")
# print(response.status_code)

# 500
# response = requests.post("https://playground.learnqa.ru/api/get_500")
# print(response.status_code)
# print(response.text)

# 404
# response = requests.post("https://playground.learnqa.ru/api/smth")
# print(response.status_code)
# print(response.text)

# Параметр - allow_redirects: если значение True - следуем до конечной точки по редиректу; если False - не пойдем на редирект, будут данные только первого запроса
# 301 - редирект - всегда будет редиректить
# response = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=False)
# print(response.status_code)

# Должно быть 200
response = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
# Кладем все данные, которые вернулись после запроса, достаем 1й
first_response = response.history[0]
# Информация по последнему уже в response
second_response = response
print(first_response.url)
print(second_response.url)
print(response.status_code)

# 302 - редирект (move temporary) - времменный, в любой момент может исчезнуть
