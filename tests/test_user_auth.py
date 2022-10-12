from datetime import datetime
import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time


class TestUserAuth(BaseCase):
    exclude_params = [
        "wrong_username",
        "wrong_password"
    ]

    def setup(self):
        self.host = 'https://stores-tests-api.herokuapp.com'
        base_part = "testqa"
        domain = "test.com"
        random_part = datetime.now().strftime("/%d-%m-%Y/%H:%M:%S")
        self.email = f"{base_part}{random_part}@{domain}"
        self.data = {
            "username": self.email,
            "password": "Password"
        }
        time.sleep(1)
        response = requests.post(self.host + "/register", data=self.data)

        Assertions.assert_status_code(response, 201)
        Assertions.assert_json_has_key(response, "uuid")
        Assertions.assert_json_value_by_name(
            response,
            'message',
            'User created successfully.',
            f"Unexpected response message! Expected: 'User created successfully.' Actual: {response.json()['message']}"
        )

    def test_auth_user(self):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "username": self.data['username'],
            "password": "Password"
        }

        response_login = requests.post(self.host + "/auth", json=data, headers=headers)
        # print(response_login.text)
        Assertions.assert_status_code(response_login, 200)
        Assertions.assert_json_has_key(response_login, 'access_token')
        self.access_token = self.get_json_value(response_login, 'access_token')

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        headers = {"Content-Type": "application/json"}
        if condition == 'wrong_username':
            response_login = requests.post(self.host + '/auth', json={
                "username": '',
                "password": "Password"
            }, headers=headers)

        else:
            response_login = requests.post(self.host + '/auth', json={
                "username": self.data['username'],
                "password": ""
            }, headers=headers)
        Assertions.assert_status_code(response_login, 401)
        Assertions.assert_json_has_key(response_login, 'error')
        Assertions.assert_json_value_by_name(
            response_login,
            'description',
            'Invalid credentials',
            f"Unexpected response message! Expected:'Invalid credentials' Actual:{response_login.json()['description']}"
        )
