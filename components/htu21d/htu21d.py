from adafruit_htu21d import HTU21D

# "sudo pip3 install adafruit-circuitpython-htu21d"
# https://learn.adafruit.com/adafruit-htu21d-f-temperature-humidity-sensor/python-circuitpython

class Htu21d:

    def __init__(self, i2c, address=0x40):
        self.htu = HTU21D(i2c, address)

    def get_temperature(self):
        return self.htu.temperature

    def get_humidity(self):
        return self.htu.relative_humidity
