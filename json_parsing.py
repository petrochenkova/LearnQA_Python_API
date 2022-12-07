import json

string_as_json_format = '{"answer":"Hello, User"}'
# Парсинг строки. Строка превращается в объект.
obj = json.loads(string_as_json_format)

key = "answer"

if key in obj:
    print(obj[key])
else:
    print(f"Ключа {key} в JSON нет")