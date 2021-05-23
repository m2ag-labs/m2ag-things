from device.services.i2cwrapper import I2cWrapper


class Ccs811(I2cWrapper):

    def __init__(self, config, logging, i2c):
        self.edata = None
        I2cWrapper.__init__(self, config, logging, i2c)

    def set(self, val):
        t = val.split(',')
        self.device.set_environmental_data(int(t[0]), float(t[1]))
