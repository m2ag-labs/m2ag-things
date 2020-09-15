import subprocess
from pathlib import Path
# TODO: why does this give module not found here? It works
try:
    from device.hardware.helpers.config import Config
except ModuleNotFoundError:
    pass
import adafruit_veml7700


# https://www.adafruit.com/product/4162?utm_source=youtube&amp;utm_medium=videodescrip&amp;utm_campaign=newproducts&gclid=CjwKCAjwyo36BRAXEiwA24CwGVaaUUkdGNnE0tz5silh9XHsYxFG_sCalH0KaaAqhwkw4Bbo4OOIVRoCJlYQAvD_BwE
# https://github.com/adafruit/Adafruit_CircuitPython_VEML7700
# sudo pip3 install adafruit-circuitpython-veml7700
# https://circuitpython.readthedocs.io/projects/veml7700/en/latest/api.html


class Backlight:

    def __init__(self, i2c, address=0x18):
        self.veml7700 = self.veml7700 = adafruit_veml7700.VEML7700(i2c, address=address)
        self.state = 2  # state 0 = off , 1 = on, 2 = pwm_value
        self.pwm_pin = 10
        cmd = 'sudo python3 ' + str(Path.home()) + '/m2ag-labs/device/hardware/components/backlight.py ' + str(self.pwm_pin)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        process.communicate()
        # get config from file -- will be in $home/.m2ag-labs/alarmclock.json
        config = Config.get_config('backlight')
        for i in config:
            setattr(self, i, config[i])

    def save_config(self):
        #  The alarm will be daily for now -- fancier stuff later
        #  TODO: add a call to db for alarm setting -- set to current
        save = ["state"]
        data = {}
        for i in save:
            data[i] = getattr(self, i)
        Config.put_config('backlight', data)

    def get(self, val):
        if val == 'light':
            return self.veml7700.light
        if val == 'state':
            # we want to support on/off/ambient (0/1/2) (track the light sensor)
            # sensor will update on poll state.
            if self.state == 2:
                command = 'gpio -g pwm ' + str(self.pwm_pin) + ' ' + str(
                    self._valmap(self.veml7700.light, 0, 12000, 128, 1023))
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

            return self.state

    def set(self, value):
        if value[0] == 'state':
            if value[1] == 0:
                command = 'gpio -g pwm ' + str(self.pwm_pin) + ' 0'
                subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            elif value[1] == 1:
                command = 'gpio -g pwm ' + str(self.pwm_pin) + ' 1023'
                subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            self.state = value[1]
            self.save_config()

    @staticmethod
    def _valmap(value, istart, istop, ostart, ostop):
        return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
