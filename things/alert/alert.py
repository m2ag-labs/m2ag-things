from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time


# tone https://gpiozero.readthedocs.io/en/stable/api_tones.html#tone

class Alert:

    def __init__(self, config, logging):
        self.buzzer = TonalBuzzer(config['init']['pin'])
        self.alerting = False

    # This maps to https://iot.mozilla.org/schemas/#Alarm
    #
    def sound_alert(self, val='not_alert'):
        self.alerting = True
        if val == 'alert':
            self.buzzer.play(Tone("A4"))
            time.sleep(0.1)
            self.buzzer.play(Tone("G4"))
            time.sleep(0.1)
            self.buzzer.play("D4")
            time.sleep(0.1)
            self.buzzer.play("A4")
            time.sleep(0.1)
        else:
            self.buzzer.play(Tone("D4"))
            time.sleep(0.1)
            self.buzzer.play(Tone("C4"))
            time.sleep(0.1)
            self.buzzer.play("G4")
            time.sleep(0.1)
            self.buzzer.play("D4")
            time.sleep(0.1)

        self.buzzer.stop()
        self.alerting = False

    def get(self, prop):
        return getattr(self, prop)

    def set(self, value):
        self.sound_alert(value)
