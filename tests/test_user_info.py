import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "wrong_cookie"
    ]

    def setup(self):
        self.host = "https://stores-tests-api.herokuapp.com"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.data = {
            "username": "irfeoij@fjre.com",
            "password": "retrefer"
        }
        response_login = requests.post(self.host + "/auth", json=self.data, headers=self.headers)
        print(response_login.headers)
        Assertions.assert_status_code(response_login, 200)
        Assertions.assert_json_has_key(response_login, 'access_token')
        self.access_token = self.get_json_value(response_login, 'access_token')
        # print(self.access_token)

    def test_auth_user(self):
        headers = {"Authorization": "JWT " + self.access_token}
        response_workspace = requests.get(self.host + '/user_info/1', headers=headers)
        # print(response_workspace.json())
        Assertions.assert_status_code(response_workspace, 200)

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == 'no_cookie':
            response_workspace = requests.get(self.host + '/auth',
                                              headers={})

        else:
            response_workspace = requests.get(self.host + '/auth',
                                              headers={"Content-Type": "application/json"}
                                              )
        Assertions.assert_status_code(response_workspace, 200)
        # assert "id" not in response_workspace.json()['data'], f"the response mustn't have the ID with {condition}"
