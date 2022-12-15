import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
history = response.history
print(f"Количество редиректов - {len(history)}:")
for i in history:
    print(i.url)
