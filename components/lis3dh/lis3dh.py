from device.hardware.i2cwrapper import I2cWrapper


class Lis3dh(I2cWrapper):

    def __init__(self, config, logging, i2c):
        I2cWrapper.__init__(self, config, logging, i2c)

    def get(self, val):
        values = ['x', 'y', 'z']
        if val in values:
            return getattr(self.device, 'acceleration')[values.index(val)]
        else:
            return super().get(val)
