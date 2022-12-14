import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Deleting tests")
@allure.feature("Deleting")
class TestUserDelete(BaseCase):
    @allure.title("Unsuccessful deleting user with id 2")
    @allure.story("Delete user with id=2")
    @allure.description("This test doesn't delete user with id=2")
    def test_delete_user_with_id_2(self):
        base_url = "/user/2"
        login_url = "/user/login"
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        # LOGIN
        response1 = MyRequests.post(login_url, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(base_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("UTF-8") == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'

        # ASSERTING
        base_url = f"/user/2"
        response3 = MyRequests.get(base_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 200)
        assert response3.content.decode(
            "UTF-8") == '{"id":"2","username":"Vitaliy","email":"vinkotov@example.com","firstName":"Vitalii","lastName":"Kotov"}'

    @allure.title("Successful deleting just create user")
    @allure.description("This test successfully delete just create user")
    def test_delete_just_created_user(self):
        register_url = "/user/"
        login_url = "/user/login"
        # REGISTER
        register_data = self.prepare_reg_data()
        response1 = MyRequests.post(register_url, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post(login_url, data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        del_url = f"/user/{user_id}"
        response2 = MyRequests.delete(del_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response2, 200)

        # ASSERTING
        response3 = MyRequests.get(del_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 404)
        assert response3.content.decode("UTF-8") == 'User not found'

    @allure.title("Unsuccessful deleting with different user authorization")
    @allure.description("This test doesn't delete user with different user authorization")
    def test_delete_another_user(self):
        register_url = "/user/"
        login_url = "/user/login"
        # REGISTER 1
        register_data = self.prepare_reg_data()
        response1 = MyRequests.post(register_url, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_name = register_data["firstName"]
        user_id = self.get_json_value(response1, "id")

        # REGISTER 2
        register_data = self.prepare_reg_data2()
        response2 = MyRequests.post(register_url, data=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email1 = register_data["email"]
        password1 = register_data["password"]

        # LOGIN
        login_data = {
            "email": {email1},
            "password": {password1}
        }

        response3 = MyRequests.post(login_url, data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # DELETE
        del_url = f"/user/{user_id}"
        response4 = MyRequests.delete(del_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 200)

        # ASSERTING
        base_url = f"/user/{user_id}"
        response5 = MyRequests.get(base_url, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response5, 200)
        assert response5.content.decode("UTF-8") == '{"username":"' + first_name + '"}'
