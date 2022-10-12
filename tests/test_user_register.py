import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserRegister(BaseCase):
    def setup(self):
        base_part = "testqa"
        domain = "test.com"
        random_part = datetime.now().strftime("/%d-%m-%Y/%H:%M:%S")[:19]
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            "username": self.email,
            "password": "Password"
        }

        response = requests.post("https://stores-tests-api.herokuapp.com/register", data=data)
        Assertions.assert_status_code(response, 201)
        Assertions.assert_json_has_key(response, "uuid")
        Assertions.assert_json_value_by_name(
            response,
            'message',
            'User created successfully.',
            f"Unexpected response message! Expected: 'User created successfully.'Actual: {response.json()['message']}")

    def test_create_user_with_existing_email(self):
        data = {
            "username": self.email,
            "password": "Password"
        }
        response = requests.post("https://stores-tests-api.herokuapp.com/register", data=data)
        print(response.json())
        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_has_key(response, "uuid")
        Assertions.assert_json_value_by_name(
            response,
            'message',
            "A user with that username already exists",
            f"Unexpected response message! Expected: 'A user with that username already exists' "
            f"Actual: {response.json()['message']}")
