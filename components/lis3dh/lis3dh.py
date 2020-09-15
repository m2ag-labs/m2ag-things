import adafruit_lis3dh

# sudo pip3 install adafruit-circuitpython-lis3dh
# https://circuitpython.readthedocs.io/projects/lis3dh/en/latest/api.html


class Lis3dh:

    def __init__(self, i2c, address=0x18):
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=address)

    def get(self, val):
        if val == 'orient':
            x, y, z = [value / adafruit_lis3dh.STANDARD_GRAVITY for value in self.lis3dh.acceleration]
            if abs(z) > 0.890:
                return 0
            if abs(y) > 0.890:
                return 1
            if abs(x) > 0.890:
                return 2
            else:
                return 3


