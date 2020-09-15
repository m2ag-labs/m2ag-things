import subprocess
from pathlib import Path

# import time

# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-8-using-a-servo-motor/software
# http://wiringpi.com/the-gpio-utility/
"""
gpio pwm-ms
gpio pwmc 192
gpio pwmr 2000
--- Gives range between 100 and 200
gpio -g mode 12 pwm
gpio -g mode 13 pwm
"""
#  TODO: replace wiring pi
"""
https://learn.adafruit.com/adafruit-raspberry-pi-lesson-9-controlling-a-dc-motor/the-pwm-kernel-module
Want to use hardware pwm on the pi. 
Currently wiring pi can be made to work, but have init with a python script run as sudo. 
"""


class Raspipwm:

    def __init__(self):
        # uses pwm 12 and 13 to drive a servo motor.
        # 18 can be added but I plan on using that for a neopixel.
        self.pwm12 = 0
        self.pwm13 = 0
        home = str(Path.home())
        cmd = 'sudo python3 ' + home + '/m2ag-labs/device/hardware/components/init_raspi_hw_pwm.py'
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        process.communicate()

    def get(self, pin):
        if pin == 12:
            return self.pwm12
        if pin == 13:
            return self.pwm13
        return None

    """
    Uses value helper index
    pin = value[0]
    value to set = value[1]
    """

    def set(self, value):
        if value[0] == 12:
            self.pwm12 = value[1]
        if value[0] == 13:
            self.pwm13 = value[1]
        command = '/usr/bin/gpio -g pwm ' + str(value[0]) + " " + str(value[1])
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        process.communicate()
