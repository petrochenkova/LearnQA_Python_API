# Запуск - python3 -m pytest -s ex10.py -k "test_my_test"
def test_my_test():
    phrase = input("Set a phrase: ")
    assert len(phrase)<15, f'Длина фразы "{phrase}" более 15 символов'
