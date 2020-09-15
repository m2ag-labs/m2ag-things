from webthing import (Thing)
from tornado import ioloop


# https://iot.mozilla.org/schemas/#PushButton


class Buttons(Thing):

    def __init__(self, conf, logging, component):
        Thing.__init__(
            self,
            conf['init']['id'],
            conf['init']['title'],
            conf['init']['type'],
            conf['init']['description']
        )

        self.component = component
        self.logging = logging
        self.main_loop = ioloop.IOLoop.current()
        self.component.red_button.when_pressed = self.red_button_call
        self.component.green_button.when_pressed = self.green_button_call
        self.component.red_button.when_released = self.red_button_released_call
        self.component.green_button.when_released = self.green_button_released_call

    def red_button_call(self):
        self.main_loop.add_callback(self.send_red_update)

    def send_red_update(self):
        self.set_property('red_button', True)

    def red_button_released_call(self):
        self.main_loop.add_callback(self.send_red_released_update)

    def send_red_released_update(self):
        self.set_property('red_button', False)

    def green_button_call(self):
        self.main_loop.add_callback(self.send_green_update)

    def send_green_update(self):
        self.set_property('green_button', True)

    def green_button_released_call(self):
        self.main_loop.add_callback(self.send_green_released_update)

    def send_green_released_update(self):
        self.set_property('green_button', False)
