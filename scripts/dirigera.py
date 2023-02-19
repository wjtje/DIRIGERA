import typing

import requests
import urllib3
import urllib3.exceptions


class Client:

    def __init__(self, host: str, access_token: str, warn_insecure: bool = False):
        self._base_url = 'https://%s:8443/v1/' % host
        self._access_token = access_token
        self._session = requests.Session()
        self._session.verify = False
        if not warn_insecure:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _request(self, path: str, method: str = None, params: typing.Any = None):
        headers = {'Authorization': 'Bearer ' + self._access_token}
        if method is None:
            method = 'GET' if params is None else 'PUT'
        response = self._session.request(method=method, url=self._base_url + path, json=params, headers=headers)
        response.raise_for_status()
        return response.json() if method == 'GET' else None

    def list_devices(self):
        return self._request('devices/')

    def edit_device_state(self, id: str, new_state: typing.Dict):
        return self._request(path='devices/%s' % id, method='PATCH', params=[new_state])


# 1. To find host name of gateway:
# mdns-scan
# Domain name: XXX._ihsp._tcp.local -> host "XXX.local"

# 2. Use get_auth_token.py to generate auth token.

# 3. Turn on light:
# client = Client(host, access_token)
# client.edit_device_state(id='323cdd30-b08e-11ed-9beb-342eb7047153_1', new_state={'attributes': {'isOn': True}})
