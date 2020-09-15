import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# sudo pip3 install adafruit-circuitpython-ads1x15
# https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython
# https://circuitpython.readthedocs.io/projects/ads1x15/en/latest/
# sudo pip3 install adafruit-circuitpython-ads1x15

class Ads1015:
    # setup for single ended on 4 channels
    def __init__(self, i2c, address=0x48):
        self.ads = ADS.ADS1015(i2c, address=address)
        self.ch0 = AnalogIn(self.ads, ADS.P0)
        self.ch1 = AnalogIn(self.ads, ADS.P1)
        self.ch2 = AnalogIn(self.ads, ADS.P2)
        self.ch3 = AnalogIn(self.ads, ADS.P3)

    def get(self, channel):
        return getattr(self, channel).voltage
