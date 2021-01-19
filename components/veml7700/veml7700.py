import adafruit_veml7700

# https://www.adafruit.com/product/4162?utm_source=youtube&amp;utm_medium=videodescrip&amp;utm_campaign=newproducts&gclid=CjwKCAjwyo36BRAXEiwA24CwGVaaUUkdGNnE0tz5silh9XHsYxFG_sCalH0KaaAqhwkw4Bbo4OOIVRoCJlYQAvD_BwE
# https://github.com/adafruit/Adafruit_CircuitPython_VEML7700
# sudo pip3 install adafruit-circuitpython-veml7700
# https://circuitpython.readthedocs.io/projects/veml7700/en/latest/api.html
# address = 0x18

class Veml7700:

    def __init__(self, i2c, config, logging):
        self.veml7700 = adafruit_veml7700.VEML7700(i2c, address=config['init']['address'])

    def get(self, val):
        if val == 'light':
            return self.veml7700.light
