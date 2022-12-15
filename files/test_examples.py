class TestExample:
    def test_check_math(self):
        a = 5
        b = 9
        expected_sum = 14
        assert a+b == expected_sum, f"Sum of variables a and b is not equal to {expected_sum}"
# Запуск - python3 -m pytest test_examples.py -k "test_check_math"
    def test_check_math2(self):
        a = 5
        b = 91
        expected_sum = 14
        assert a+b == expected_sum, f"Sum of variables a and b is not equal to {expected_sum}"