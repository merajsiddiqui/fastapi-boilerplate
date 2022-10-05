from requests import request
from decouple import config
import json


class MobileSMS:
    _api_key = ''

    def __init__(self):
        self._api_key = config('SMS_API_KEY')

    def send_otp(self, mobile_number: str) -> bool | Exception:
        endpoint = '{}/AUTOGEN/:otp_template_name'.format(mobile_number)
        self.__request_2_factor(endpoint)
        return True

    def validate_otp(self, mobile_number: str, otp: str) -> bool | Exception:
        endpoint = 'VERIFY3/{}/{}'.format(mobile_number, otp)
        self.__request_2_factor(endpoint)
        # Mark user as verified
        return True

    def __request_2_factor(self, endpoint: str) -> bool | Exception:
        request_uri = 'https://2factor.in/API/V1/{}/SMS/{}'.format(self._api_key, endpoint)
        response = request("GET", request_uri)
        response = json.loads(response.json())
        if response.status != "Success":
            raise Exception(response.Details)
        return True
