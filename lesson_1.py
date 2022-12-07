import requests

responce = requests.get("https://playground.learnqa.ru/api/get_text")
print(responce.text)

print("Hello from Anastasiia!")
