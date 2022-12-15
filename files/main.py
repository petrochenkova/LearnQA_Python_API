from json.decoder import JSONDecodeError
import requests

# # Payload - словарь параметров
# payload = {"name": "User"}
# responce = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
# print(responce.text)

# responce = requests.get("https://playground.learnqa.ru/api/hello", params={"name": "User"})

responce = requests.get("https://playground.learnqa.ru/api/get_text")
print(responce.text)

try:
    parsed_responce_text = responce.json()
    print(parsed_responce_text["answer"])
except JSONDecodeError:
    print("Responce is not а JSON format")

