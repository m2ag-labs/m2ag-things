import requests
from datetime import datetime
import json

DEVICE_URL = 'https://smartdevicemanagement.googleapis.com/v1/'
AUTH_URL = 'https://www.googleapis.com/oauth2/v4/'


class Nest:

    def __init__(self, config, logging):
        self.logging = logging
        self.access_token = None
        self.access_token_next = 0
        self.config = config
        self.data = {"status": -1, "message": "no data", "devices": {}}

    def get_auth(self):

        if datetime.timestamp(datetime.now()) < self.access_token_next:
            return True

        url = AUTH_URL + f'token?client_id={self.config["oauth-client"]}'
        url += f'&client_secret={self.config["oauth-secret"]}'
        url += f'&refresh_token={self.config["refresh-token"]}&grant_type=refresh_token'

        response = requests.request("POST", url, headers={}, data={})
        try:
            j = json.loads(response.text)
            self.access_token = j['access_token']
            self.access_token_next = datetime.timestamp(datetime.now()) + j['expires_in'] * 1000
        except (UnicodeDecodeError, AttributeError):
            self.access_token = None
            self.access_token_next = 0
            self.data['message'] = "json or attribute decode error"
            self.logging.warning("auth json decode/attribute error")
            self.data['status'] = 0
            return False

        self.data['status'] = 1
        self.data['message'] = 'active'
        return True

    def get_data(self):
        if self.get_auth():
            url = DEVICE_URL + f'enterprises/{self.config["project-id"]}/devices'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            }
            # TODO: try catch this
            response = requests.request("GET", url, headers=headers, data={})
            if response.status_code == 401:
                self.access_token_next = 0

            found = False
            try:
                j = json.loads(response.text)
                for device in j['devices']:
                    if device['name'] in self.config['devices']:
                        self.data['devices'][self.config['devices'][device['name']]] = device['traits']
                        found = True
                    else:
                        self.logging.warning('unknown device ' + device['name'])
            except (UnicodeDecodeError, KeyError):
                self.data['message'] = "dev json or key error"
                self.logging.warning("device json or key error")
                self.data['status'] = 0
                return False

            self.data['status'] = 1  # at least one found
            if found:
                self.data['message'] = 'active'
            else:
                self.data['message'] = "no devices returned"

    def get_trait(self, dev, prop):
        if dev in self.data['devices']:
            if prop == 'hvac':
                # noinspection PyTypeChecker
                mode = self.data['devices'][dev]['sdm.devices.traits.ThermostatHvac']['status']
                return mode.lower()
            elif prop == 'timer':
                # noinspection PyTypeChecker
                if 'timerTimeout' in self.data['devices'][dev]['sdm.devices.traits.Fan']:
                    # noinspection PyTypeChecker
                    dt_str = self.data['devices'][dev]['sdm.devices.traits.Fan']['timerTimeout']
                    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ')
                    return (dt - datetime.utcnow()).seconds / 60
                else:
                    return 0
            self.data['message'] = prop + " not found in data['device'][" + dev + "]"
        else:
            self.data['message'] = dev + " not found in data[device]"
        return -1

    def set_trait(self, dev, prop, value):
        if dev not in self.data['devices']:
            self.data['message'] = dev + " not found in data[device]"
        else:
            device_id = None
            for i in self.config['devices']:
                if self.config['devices'][i] == dev:
                    device_id = i
            url = DEVICE_URL + f'{device_id}:executeCommand'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.access_token}'
            }
            if prop == 'timer':
                # noinspection PyTypeChecker
                if self.get_auth():
                    data = {
                        "command": "sdm.devices.commands.Fan.SetTimer",
                        "params": {}
                    }
                    if value > 0:
                        data['params']['duration'] = str(value * 60) + 's'  # minutes to seconds
                        data['params']['timerMode'] = "ON"
                    else:
                        data['params']['timerMode'] = "OFF"

                    requests.request("POST", url, headers=headers, data=json.dumps(data))

    def get(self, prop):
        li = self.config['devices'].values()
        for v in li:
            if prop.startswith(v):
                return self.get_trait(v, prop[len(v) + 1:])

        if prop == 'status':  # calls to status trigger a poll
            self.get_data()

        if prop in self.data and self.data['status'] > 0:
            return self.data[prop]
        else:
            if self.data['status'] > 0:
                self.logging.warning('no data for ' + prop)
            if prop == 'message':  # need to watch the type of the thing prop.
                return 'no data'
            else:
                return -1

    def set(self, value):
        li = self.config['devices'].values()
        for v in li:
            if value[0].startswith(v):
                self.set_trait(v, value[0][len(v) + 1:], value[1])
                self.get_data()
