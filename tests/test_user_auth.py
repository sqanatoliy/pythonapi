import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserAuth(BaseCase):
    # PARAMETERS FOR NEGATIVE TEST
    exclude_params = [
        "wrong_username",
        "wrong_password"
    ]

    def setup(self):
        # CREATE DATA FOR REGISTRATION
        self.register_data = self.prepare_registration_data()

    def test_auth_user(self):
        # REGISTER USER
        response = MyRequests.post("/register", data=self.register_data)
        expected_fields = ['message', 'uuid']
        Assertions.assert_json_has_keys(response, expected_fields)
        Assertions.assert_status_code(response, 201)

        # LOGIN USER
        response_login = MyRequests.post("/auth", json=self.register_data)

        Assertions.assert_status_code(response_login, 200)
        Assertions.assert_json_has_key(response_login, 'access_token')
        self.access_token = self.get_json_value(response_login, 'access_token')

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        # GET RESPONSE WITHOUT USERNAME
        if condition == 'wrong_username':
            response_login = MyRequests.post('/auth', json={
                "username": '',
                "password": "Password"
            })

        else:
            # GET RESPONSE WITHOUT PASSWORD
            response_login = MyRequests.post('/auth', json={
                "username": self.register_data['username'],
                "password": ""
            })

        expected_fields = ['description', 'error', 'status_code']
        Assertions.assert_json_has_keys(response_login, expected_fields)
        Assertions.assert_json_value_by_name(
            response_login,
            'description',
            'Invalid credentials',
            f"Unexpected response message! Expected:'Invalid credentials' Actual:{response_login.json()['description']}"
        )
        Assertions.assert_status_code(response_login, 401)
