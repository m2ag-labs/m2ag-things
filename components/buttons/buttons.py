from gpiozero import Button


# https://gpiozero.readthedocs.io/en/stable/api_input.html

class Buttons:

    def __init__(self):
        # print("button init")
        self.green_button = Button(12)
        self.red_button = Button(16)

    def get(self, button):
        return getattr(self, button).is_pressed
