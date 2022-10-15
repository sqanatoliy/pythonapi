import json.decoder
from requests import Response
from datetime import datetime

"""This class includes general methods that we can use in other classes."""
"""Other classes will follow the BaseCase methods"""


class BaseCase:

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f" Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with the name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in JSON Format. Response text is "{response.text}"'
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "testqa"
            domain = "test.com"
            random_part = datetime.now().strftime("/%d-%m-%Y/%H:%M:%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            "username": email,
            "password": "Password"
        }

    def prepare_user_data(self, user_uuid):
        return {
            "phone": f"{user_uuid * 10}",
            "email": f"{user_uuid}@test.test",
            "address": {
                "city": f"Lviv",
                "street": f"Svobody {user_uuid}",
                "home_number": f"{user_uuid}"
            }
        }
