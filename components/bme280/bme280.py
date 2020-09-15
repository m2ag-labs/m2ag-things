import adafruit_bme280

# sudo pip3 install adafruit-circuitpython-bme280

class Bme280:

    def __init__(self, i2c, address=0x76):
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address)

    def get(self, value):
        if value == 'temperature':
            return self.bme280.temperature
        if value == 'humidity':
            return self.bme280.humidity
        if value == 'pressure':
            return self.bme280.pressure
