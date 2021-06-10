from device.services.i2cwrapper import I2cWrapper


class Bme680(I2cWrapper):
    HUM_WEIGHT = .25
    HUM_REFERENCE = 40
    GAS_WEIGHT = .75
    GAS_UPPER_LIMIT = 84000
    GAS_LOWER_LIMIT = 5000

    def __init__(self, config, logging, i2c):
        I2cWrapper.__init__(self, config, logging, i2c)
        self.gas_score = 0
        self.average = []

    def get(self, val):
        if val == 'iaq':
            try:
                data = int((100 - (self.get_hum_score() + self.get_gas_score())) * 5)
                self.average.append(data)
                if len(self.average) > 60:
                    self.average.pop(0)
            except RuntimeError:
                data = -1
        elif val == 'iaq_avg':
            data = int(sum(self.average) / len(self.average))

        else:
            data = super().get(val)

        return data

    def get_gas_ref(self):
        readings = 10
        gas = 0
        for x in range(readings):
            gas += self.device.gas
        return gas / readings

    def get_hum_score(self):
        hum = self.device.relative_humidity
        if 38 <= hum <= 42:
            hum_score = 0.25 * 100
        elif hum < 38:
            hum_score = 0.25 / self.HUM_REFERENCE * hum * 100
        else:
            hum_score = ((-0.25 / (100 - self.HUM_REFERENCE) * hum) + 0.416666) * 100
        return hum_score

    def get_gas_score(self):
        gas_reference = self.get_gas_ref()
        if gas_reference > self.GAS_UPPER_LIMIT: gas_reference = self.GAS_UPPER_LIMIT
        if gas_reference < self.GAS_LOWER_LIMIT: gas_reference = self.GAS_LOWER_LIMIT
        gas_score = (0.75 / (self.GAS_UPPER_LIMIT - self.GAS_LOWER_LIMIT) * gas_reference - (
                self.GAS_LOWER_LIMIT * (0.75 / (self.GAS_UPPER_LIMIT - self.GAS_LOWER_LIMIT)))) * 100

        return gas_score
