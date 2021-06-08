from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, Servo
from gpiozero import Button
from gpiozero import LED


# https://gpiozero.readthedocs.io/en/stable/api_input.html
# https://gpiozero.readthedocs.io/en/stable/api_output.html#regular-classes
# simplified access to some gpiozero functionality. We are mainly interested in just
# getting reliable inputs and out puts -- we let node-red or home automation to provide
# functionality.

class Pigpio:

    def __init__(self, config, logging):
        # TODO: PiGPIO daemon must be running and port moved to 8889
        # TODO: add more config options for servo
        # TODO: what other gpiozero types?
        Device.pin_factory = PiGPIOFactory(port=8889)
        self.attr = config['attr']['input']
        self.logging = logging
        if 'input' in config['init']:
            for i in config['init']['input']:
                short = config['init']['input'][i]
                try:
                    setattr(self, i, Button(pin=short['pin'], pull_up=short['pull_up']))
                except:
                    self.logging.error(f'GPIO: {i} would not initialize')
        if 'output' in config['init']:
            for i in config['init']['output']:
                short = config['init']['output'][i]
                try:
                    setattr(self, i,
                        LED(pin=short['pin'], active_high=short['active_high'], initial_value=short['initial_value']))
                except:
                    self.logging.error(f'GPIO: {i} would not initialize')

        if 'servo' in config['init']:
            for i in config['init']['servo']:
                short = config['init']['servo'][i]
                try:
                    setattr(self, i, Servo(pin=short['pin']))
                except:
                    self.logging.error(f'GPIO: {i} would not initialize')

    def get(self, target):
        if hasattr(self, target):
            if type(getattr(self, target[0])) is LED:
                return getattr(self, target[0]).value
            if type(getattr(self, target[0])) is Button:
                return getattr(self, target[0]).is_pressed()
            if type(getattr(self, target[0])) is Servo:
                return (getattr(self, target[0]).value + 1) * 100
        else:
            self.logging.error(target + " gpio not found")
            return -1

    def set(self, target):
        if type(getattr(self, target[0])) is LED:
            getattr(self, target[0]).value = target[1]
        if type(getattr(self, target[0])) is Servo:
            getattr(self, target[0]).value = (2.0 * (target[1] / 100.0)) - 1.0
