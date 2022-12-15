import requests
import pytest


parameters = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',{'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',{'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',{'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0', {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',{'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
    ]


# Первое - имя переменной, в которую pytest будет передавать данные. Второе - переменная, в которой эти данные сейчас хранятся
@pytest.mark.parametrize("agent,expected_results", parameters)
def test_user_agent(agent,expected_results):

    url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

    response = requests.get(url, headers={"User-Agent": agent})

    response_json = response.json()

    assert "platform" in response_json, "No parameter 'platform' in response"
    assert response_json["platform"] == expected_results["platform"], f'Wrong platform parameter. Actual - {response_json["platform"]}, Expexted - {expected_results["platform"]}'

    assert "browser" in response_json, "No parameter 'browser' in response"
    assert response_json["browser"] == expected_results["browser"],f'Wrong browser parameter. Actual - {response_json["browser"]}, Expexted - {expected_results["browser"]}'


    assert "device" in response_json, "No parameter 'device' in response"
    assert response_json["device"] == expected_results["device"],f'Wrong device parameter. Actual - {response_json["device"]}, Expexted - {expected_results["device"]}'