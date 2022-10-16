import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User info cases")
class TestUserInfo(BaseCase):
    exclude_params = [
        "no_token",
        "no_user_data"
    ]

    def setup(self):
        # REGISTER
        self.register_data = self.prepare_registration_data()
        response_register = MyRequests.post("/register", data=self.register_data)
        expected_fields = ['message', 'uuid']
        Assertions.assert_json_has_keys(response_register, expected_fields)
        Assertions.assert_status_code(response_register, 201)

        self.user_uuid = str(self.get_json_value(response_register, 'uuid'))
        self.user_data = self.prepare_user_data(self.user_uuid)

        # LOGIN AND GET ACCESS TOKEN
        response_login = MyRequests.post("/auth", json=self.register_data)
        Assertions.assert_status_code(response_login, 200)
        Assertions.assert_json_has_key(response_login, 'access_token')
        access_token = self.get_json_value(response_login, 'access_token')

        # HEADERS WITH ACCESS TOKEN
        self.headers = {"Authorization": "JWT " + access_token}

    @allure.description('This test successfully post user info')
    def test_post_user_info(self):
        # CREATE USER DATA
        response_user_info_post = MyRequests.post('/user_info/' + self.user_uuid, json=self.user_data,
                                                  headers=self.headers)
        Assertions.assert_status_code(response_user_info_post, 200)
        Assertions.assert_json_value_by_name(
            response_user_info_post,
            'message',
            'User info created successfully.',
            f"Unexpected response message! Expected: 'User info created successfully.' Actual: {response_user_info_post.json()['message']}"
        )

    @allure.description('This test successfully update user info')
    def test_put_user_info(self):
        # CREATE USER DATA
        response_user_info_post = MyRequests.post('/user_info/' + self.user_uuid, json=self.user_data,
                                                  headers=self.headers)
        Assertions.assert_status_code(response_user_info_post, 200)
        Assertions.assert_json_value_by_name(
            response_user_info_post,
            'message',
            'User info created successfully.',
            f"Unexpected response message! Expected: 'User info created successfully.' Actual: {response_user_info_post.json()['message']}"
        )

        # EDIT USER DATA
        new_user_data = {
            "phone": f"{self.user_uuid * 9}",
            "email": f"{self.user_uuid}@updated.test",
            "address": {
                "city": f"Lviv {self.user_uuid}",
                "street": f"Svobody updated {self.user_uuid}",
                "home_number": f"updated {self.user_uuid}"
            }
        }
        response_user_info_put = MyRequests.put('/user_info/' + self.user_uuid, json=new_user_data,
                                                headers=self.headers)
        Assertions.assert_status_code(response_user_info_put, 200)
        Assertions.assert_json_value_by_name(
            response_user_info_put,
            'message',
            'User info updated successfully.',
            f"Unexpected response message! Expected: 'User info updated successfully.' Actual: {response_user_info_post.json()['message']}"
        )

        # CHECK NEW USER  DATA
        response_new_user_info_get = MyRequests.get('/user_info/' + self.user_uuid,
                                                    headers=self.headers)
        expected_fields = ["city", "street", "userID", "phone", "email"]
        Assertions.assert_json_has_keys(response_new_user_info_get, expected_fields)
        Assertions.assert_json_value_by_name(
            response_new_user_info_get,
            'email',
            f"{new_user_data['email']}",
            f"Unexpected response message! Expected: {self.user_uuid}@test.test Actual: {response_new_user_info_get.json()['email']}"
        )
        Assertions.assert_status_code(response_new_user_info_get, 200)

    @allure.description('This test successfully get user info')
    def test_get_user_info(self):
        # CREATE USER DATA
        response_user_info_post = MyRequests.post('/user_info/' + self.user_uuid, json=self.user_data,
                                                  headers=self.headers)
        Assertions.assert_status_code(response_user_info_post, 200)

        # GET USER DATA
        response_user_info_get = MyRequests.get('/user_info/' + self.user_uuid,
                                                headers=self.headers)
        expected_fields = ["city", "street", "userID", "phone", "email"]
        Assertions.assert_json_has_keys(response_user_info_get, expected_fields)
        Assertions.assert_json_value_by_name(
            response_user_info_get,
            'email',
            f"{self.user_data['email']}",
            f"Unexpected response message! Expected: {self.user_uuid}@test.test Actual: {response_user_info_get.json()['email']}"
        )
        Assertions.assert_status_code(response_user_info_get, 200)

    @allure.description('This test unsuccessfully get user info')
    @pytest.mark.parametrize('condition', exclude_params)
    def test_get_user_info_negative(self, condition):
        # GET RESPONSE WITHOUT USER DATA
        if condition == 'no_user_data':
            response_user_info = MyRequests.get('/user_info/' + self.user_uuid,
                                                headers=self.headers)
            Assertions.assert_status_code(response_user_info, 404)
            Assertions.assert_json_value_by_name(
                response_user_info,
                'message',
                'User info not found',
                f"Unexpected response message! Expected: 'User info not found' Actual: {response_user_info.json()['message']}"
            )
            Assertions.assert_json_has_not_key(response_user_info, 'email')
        else:
            # GET RESPONSE WITHOUT ACCESS TOKEN
            headers = {"Content-Type": "application/json"}
            response_user_info = MyRequests.get('/user_info/' + self.user_uuid, headers=headers)
            expected_fields = ["description", "error", "status_code"]
            Assertions.assert_json_has_keys(response_user_info, expected_fields)
            Assertions.assert_json_value_by_name(
                response_user_info,
                'error',
                'Authorization Required',
                f"Unexpected response message! Expected: 'Authorization Required' Actual: {response_user_info.json()['error']}"
            )
            Assertions.assert_json_has_not_key(response_user_info, 'email')
            Assertions.assert_status_code(response_user_info, 401)
