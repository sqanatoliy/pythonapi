import os


class Environment:
    DEV = 'dev'
    PROD = 'prod'

    URLS = {
        DEV: 'https://stores-tests-api.herokuapp.com',
        PROD: 'https://stores-tests-api.herokuapp.com/prod_api'
    }

    try:
        env = os.environ['ENV']
    except KeyError:
        env = DEV

    # def __int__(self):
    #     try:
    #         self.env = os.environ['ENV']
    #     except KeyError:
    #         self.env = self.DEV

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Unknown value of ENV variable {self.env}")


ENV_OBJECT = Environment()
