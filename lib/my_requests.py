import requests
from lib.logger import Logger


class MyRequests:
    @staticmethod
    def post(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, json, headers, cookies, 'POST')

    @staticmethod
    def get(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, json, headers, cookies, 'GET')

    @staticmethod
    def put(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, json, headers, cookies, 'PUT')

    @staticmethod
    def delete(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, json, headers, cookies, 'DELETE')

    @staticmethod
    def _send(url: str, data: dict, json: dict, headers: dict, cookies: dict, method: str):

        url = f"https://stores-tests-api.herokuapp.com{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}
        if data is None:
            data = {}
        if json is None:
            json = {}

        Logger.add_request(url, data, json, headers, cookies, method)

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, data=data, json=json, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(response)

        return response
