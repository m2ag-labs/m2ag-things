import requests
from datetime import datetime
import json

URL_ROOT = 'https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json'


class Airnow:

    def __init__(self, config, logging):
        self.config = config
        self.data = {}
        self.next_update = 0

    # This maps to https://iot.mozilla.org/schemas
    #
    def get_data(self):
        url = f'{URL_ROOT}&zipCode={self.config["zipCode"]}&distance={self.config["distance"]}&API_KEY={self.config["apiKey"]}'
        response = requests.request("GET", url, headers={}, data={})
        j = json.loads(response.text)
        self.data['pm2'] = -1
        self.data['ozone'] = -1
        self.data['hour_observed'] = -1
        self.data['status'] = 0
        self.data['message'] = 'no pm2.5 data available'
        # use the highest of the measurements
        for i in j:
            if i['ParameterName'] == 'PM2.5':
                self.data['pm2'] = i['AQI']
                self.data['hour_observed'] = i['HourObserved']
                self.data['status'] = 1
                self.data['message'] = 'pm2.5 data received'
            if i['ParameterName'] == 'O3':
                self.data['ozone'] = i['AQI']

    def get(self, prop):
        # TODO: cache until update time
        """if datetime.now().timestamp() > self.next_update:
            self.get_data()
            # poll it every 10 minutes."""
        if prop == 'status':
            self.get_data()

        if prop in self.data:
            return self.data[prop]
        else:
            if prop == 'message':  # need to watch the type of the thing prop.
                return 'no message set'
            else:
                return -1

    def set(self, value):
        pass
