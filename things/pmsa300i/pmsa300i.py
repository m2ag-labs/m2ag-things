# adafruit-circuitpython-pm25
from device.services.i2cwrapper import I2cWrapper


class Pmsa300i(I2cWrapper):

    def __init__(self, config, logging, i2c):
        I2cWrapper.__init__(self, config, logging, i2c)
        self.average = []

    def get(self, val):
        if val == 'pm2':
            try:
                aqdata = self.device.read()
                data = aqdata["pm25 env"]
                self.average.append(data)
                if len(self.average) > 60:
                    self.average.pop(0)
            except RuntimeError:
                data = -1
        elif val == 'avg':
            data = int(sum(self.average) / len(self.average))

        else:
            data = super().get(val)

        return data
