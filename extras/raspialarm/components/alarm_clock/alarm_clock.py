from datetime import datetime
import subprocess
import time
from pathlib import Path
import RPi.GPIO as GPIO
from device.hardware.helpers.config import Config


# tone https://gpiozero.readthedocs.io/en/stable/api_tones.html#tone

class Alarm_clock:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        # Hepatic output
        self.pwm_pin = 12  # this gets overridden from config
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.hepatic = GPIO.PWM(self.pwm_pin, 100)
        self.hepatic.start(0)
        # alarm stuff
        self.alarm_hour = 0  # the alarm we are waiting for -- 24 hour format
        self.alarm_minute = 0

        self.alarm_enabled = False  # is the alarm enabled?
        self.alarm_snooze_hour = 0  # will not ring alarm until snooze expires
        self.alarm_snooze_minute = 0  # will not ring alarm until snooze expires
        self.alarm_snooze_active = False

        self.alarm = False  # map to alarm thing # this means the alarm time has arrived

        self.audio_enabled = True
        self.audio_active = False  # is and alarm currently sounding?
        self.audio_style = 0
        self.audio_volume_current = 50
        self.audio_volume_min = 50
        self.audio_volume_max = 100
        self.audio_volume_incr = 2

        self.hepatic_enabled = True
        self.hepatic_current = 50
        self.hepatic_min = 50  # Max pwm to supply to motor
        self.hepatic_max = 100  # Max pwm to supply to motor
        self.hepatic_incr = 2

        # get config from file -- will be in $home/.m2ag-labs/alarmclock.json
        config = Config.get_config('alarmclock')
        for i in config:
            setattr(self, i, config[i])

    def save_config(self):
        #  The alarm will be daily for now -- fancier stuff later
        #  TODO: add a call to db for alarm setting -- set to current
        save = ["alarm_enabled", "alarm_hour", "alarm_minute", "audio_enabled", "hepatic_enabled"]
        data = {}
        for i in save:
            data[i] = getattr(self, i)
        Config.put_config('alarmclock', data)

    # get serves as the poll for this thing
    def get(self, prop):
        if prop == 'snooze':
            return self.alarm_snooze_active
        else:
            if prop == 'alarm':
                self.poll()
            return getattr(self, prop)

    def set(self, value):
        if value[0] == 'snooze':
            if value[1] is True:
                self.snooze()
            else:
                self.alarm_snooze_active = False
        else:
            if value[0] == 'alarm':
                if value[1] is False:
                    self.audio_volume_current = self.audio_volume_min
                    self.hepatic_current = self.hepatic_min
            setattr(self, value[0], value[1])
            if value[0] in ['alarm_hour', 'alarm_minute', 'alarm_enabled']:
                self.save_config()
            if value[0] == 'alarm_enabled' and value[1] is False:
                self.alarm = False
                self.alarm_snooze_active = False

    def poll(self):

        # TODO: check for alarms here
        if self.alarm_enabled and not self.alarm:
            # compare the 24 hour time to time now.
            now = datetime.now()
            #  match hour:
            if now.hour == self.alarm_hour:
                # match the minutes
                if now.minute == self.alarm_minute:
                    self.alarm = True
        # are we snoozing?
        if self.alarm_snooze_active and self.alarm:
            now = datetime.now()
            if now.hour == self.alarm_snooze_hour:
                # match the minutes
                if now.minute == self.alarm_snooze_minute:
                    self.alarm_snooze_active = False

        if self.alarm and not self.alarm_snooze_active:
            if self.audio_enabled:
                if not self.audio_active:
                    # TODO: launch this in a thread so it won't block
                    self.audio_alarm()
            if self.hepatic_enabled:
                self.hepatic_alarm()

    def snooze(self):
        if self.alarm and not self.alarm_snooze_active:
            now = datetime.now()
            self.alarm_snooze_active = True
            m = now.minute
            h = now.hour
            if m + 5 > 60:
                m = m + 5 - 60
                if h + 1 > 23:
                    self.alarm_snooze_hour = 0
                else:
                    self.alarm_snooze_hour = h + 1
            else:
                m = m + 5
                self.alarm_snooze_hour = h
            self.alarm_snooze_minute = m

    def audio_alarm(self):
        # TODO: add tone selector as a property
        # TODO: add volume property
        # must start at lower level and increase
        self.audio_active = True  # we are playing the alarm
        vol = str(self.audio_volume_current) + '%'
        self.audio_volume_current = self.audio_volume_current + self.audio_volume_incr
        if self.audio_volume_current > self.audio_volume_max:
            self.audio_volume_current = self.audio_volume_max

        subprocess.Popen(['/usr/bin/amixer', 'set', 'PCM', vol], stdout=subprocess.PIPE)
        # we read the output as a way of slowing down the calls
        # ensures only one sound file is playing at a time.
        if self.audio_style == 0:
            sound_file = '/m2ag-labs/device/hardware/components/sounds/rooster.mp3'
        else:
            sound_file = '/m2ag-labs/device/hardware/components/sounds/pager.mp3'

        p = subprocess.Popen(['/usr/bin/omxplayer', '-o', 'alsa',
                              str(Path.home()) + sound_file],
                             stdout=subprocess.PIPE)
        line = ''
        for i in range(0, 20):
            line += str(p.stdout.readline().decode('utf-8'))
        self.audio_active = False

    def hepatic_alarm(self):
        p_max = self.hepatic_current
        # TODO: move to a thread - or some non-blocking way
        for dc in range(0, p_max + 1, 5):
            self.hepatic.ChangeDutyCycle(dc)
            time.sleep(0.01)
        self.hepatic.start(0)
        time.sleep(.05)
        for dc in range(0, p_max + 1, 5):
            self.hepatic.ChangeDutyCycle(dc)
            time.sleep(0.01)
        self.hepatic.start(0)

        self.hepatic_current = self.hepatic_current + self.hepatic_incr
        if self.hepatic_current > self.hepatic_max:
            self.hepatic_current = self.hepatic_max
