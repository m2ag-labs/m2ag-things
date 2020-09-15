from adafruit_pca9685 import PCA9685


# https://www.adafruit.com/product/815
# https://learn.adafruit.com/16-channel-pwm-servo-driver
# https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython
# https://circuitpython.readthedocs.io/projects/pca9685/en/latest/api.html
# sudo pip3 install adafruit-circuitpython-pca9685


class Pca9685:

    def __init__(self, i2c, address=0x40):
        # Create a simple PCA9685 class instance.
        self.pca9685 = PCA9685(i2c, address=address)

    def get(self, channel):
        return self.pca9685.channels[channel].duty_cycle

    def set(self, value):
        self.pca9685.channels[value[0]].duty_cycle = value[1]
