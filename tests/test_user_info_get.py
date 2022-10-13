from datetime import datetime
import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserInfo(BaseCase):
    exclude_params = [
        "no_token",
        "no_user_data"
    ]

    def setup(self):
        self.host = 'https://stores-tests-api.herokuapp.com'
        self.headers = {
            "Content-Type": "application/json"
        }
        base_part = "testqa"
        domain = "test.com"
        random_part = datetime.now().strftime("/%d-%m-%Y/%H:%M:%S")
        self.email = f"{base_part}{random_part}@{domain}"
        self.data = {
            "username": self.email,
            "password": "Password"
        }
        response_register = requests.post(self.host + "/register", data=self.data)

        Assertions.assert_status_code(response_register, 201)
        Assertions.assert_json_has_key(response_register, "uuid")
        Assertions.assert_json_value_by_name(
            response_register,
            'message',
            'User created successfully.',
            f"Unexpected response message! Expected: 'User created successfully.' Actual: {response_register.json()['message']}"
        )
        self.user_uuid = str(self.get_json_value(response_register, 'uuid'))

        response_login = requests.post(self.host + "/auth", json=self.data, headers=self.headers)
        Assertions.assert_status_code(response_login, 200)
        Assertions.assert_json_has_key(response_login, 'access_token')
        self.access_token = self.get_json_value(response_login, 'access_token')

    def test_get_user_info(self):
        headers = {"Authorization": "JWT " + self.access_token}
        self.user_data = {
            "phone": f"{self.user_uuid * 10}",
            "email": f"{self.user_uuid}@test.test",
            "address": {
                "city": f"Lviv",
                "street": f"Svobody {self.user_uuid}",
                "home_number": f"{self.user_uuid}"
            }
        }
        response_user_info_post = requests.post(self.host + '/user_info/' + self.user_uuid, json=self.user_data,
                                                headers=headers)
        # print(response_user_info_post.json())

        response_user_info_get = requests.get(self.host + '/user_info/' + self.user_uuid, headers=headers)
        Assertions.assert_status_code(response_user_info_get, 200)
        Assertions.assert_json_value_by_name(
            response_user_info_get,
            'email',
            f"{self.user_data['email']}",
            f"Unexpected response message! Expected: {self.user_uuid}@test.test Actual: {response_user_info_get.json()['email']}"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_get_negative_user_info(self, condition):
        if condition == 'no_user_data':
            headers = {"Authorization": "JWT " + self.access_token}
            response_user_info = requests.get(self.host + '/user_info/' + self.user_uuid, headers=headers)
            Assertions.assert_status_code(response_user_info, 404)
            Assertions.assert_json_value_by_name(
                response_user_info,
                'message',
                'User info not found',
                f"Unexpected response message! Expected: 'User info not found' Actual: {response_user_info.json()['message']}"
            )
        else:
            headers = {"Content-Type": "application/json"}
            response_user_info = requests.get(self.host + '/user_info/' + self.user_uuid, headers=headers)
            Assertions.assert_status_code(response_user_info, 401)
            Assertions.assert_json_value_by_name(
                response_user_info,
                'error',
                'Authorization Required',
                f"Unexpected response message! Expected: 'Authorization Required' Actual: {response_user_info.json()['error']}"
            )
