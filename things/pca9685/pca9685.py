try:
    from adafruit_pca9685 import PCA9685
except ModuleNotFoundError:
    print('*** PCA9685 driver not found ***')


# https://www.adafruit.com/product/815
# https://learn.adafruit.com/16-channel-pwm-servo-driver
# https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython
# https://circuitpython.readthedocs.io/projects/pca9685/en/latest/api.html
# sudo pip3 install adafruit-circuitpython-pca9685


class Pca9685:

    def __init__(self, i2c, config, logging):
        # Create a simple PCA9685 class instance.
        # noinspection PyBroadException
        self.logging = logging
        try:
            self.pca9685 = PCA9685(i2c, address=int(config['init']['address'], 16))
            for a in config['attr']:
                setattr(self.pca9685, a, config['attr'][a])
        except:
            self.logging.error('*** PCA9685 did not initialize ***')

    def get(self, channel):
        self.logging.debug(f'channel {channel} returns {self.pca9685.channels[channel].duty_cycle}')
        return self.pca9685.channels[channel].duty_cycle

    def set(self, value):
        self.logging.debug(f'channel {value[0]} set to {value[1]}')
        self.pca9685.channels[value[0]].duty_cycle = value[1]
