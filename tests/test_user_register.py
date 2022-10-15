from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        # CREATE USER WITH NEW DATA
        register_data = self.prepare_registration_data()
        email = register_data["username"][:24]
        register_data['username'] = email
        response = MyRequests.post("/register", data=register_data)

        expected_fields = ['message', 'uuid']
        Assertions.assert_json_has_keys(response, expected_fields)
        Assertions.assert_json_value_by_name(
            response,
            'message',
            'User created successfully.',
            f"Unexpected response message! Expected: 'User created successfully.'Actual: {response.json()['message']}"
        )
        Assertions.assert_status_code(response, 201)

    def test_create_user_with_existing_email(self):
        # CREATE USER WITH SAME DATA
        register_data = self.prepare_registration_data()
        email = register_data["username"][:24]
        register_data['username'] = email

        response = MyRequests.post("/register", data=register_data)
        expected_fields = ['message', 'uuid']
        Assertions.assert_json_has_keys(response, expected_fields)
        Assertions.assert_json_value_by_name(
            response,
            'message',
            "A user with that username already exists",
            f"Unexpected response message! Expected: 'A user with that username already exists' "
            f"Actual: {response.json()['message']}")
        Assertions.assert_status_code(response, 400)
