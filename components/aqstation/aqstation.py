import PyCmdMessenger
import time
import json
import serial


class Aqstation:

    def __init__(self, config, logging):
        self.c = None
        self.arduino = None
        self.config = config
        self.logging = logging
        self.data = {'status': 0, 'message': 'not connected'}
        self.last_update = 0
        self.update_delay = 2000
        self.commands = [["poll_all", ""],
                         ["report_all", "s*"],
                         ["set_offsets", "s*"],
                         ["error", "s"]]

        self.connect()

    def connect(self):
        try:
            self.arduino = PyCmdMessenger.ArduinoBoard(self.config["serial_port"], baud_rate=57600)
            self.c = PyCmdMessenger.CmdMessenger(self.arduino, self.commands)
            self.data['status'] = 1
            self.data['message'] = 'connected'
            time.sleep(2)
        except serial.serialutil.SerialException:
            self.data['status'] = -1
            self.data['message'] = 'no arduino found'
            print()
            self.logging.warning('no arduino found')
            self.arduino = None

    # This maps to https://iot.mozilla.org/schemas
    #

    def get_data(self):
        try:
            self.c.send("poll_all")
            msg = self.c.receive()
        except (serial.serialutil.SerialException, AttributeError):
            self.logging.warning('send/receive error -- attempt reconnect')
            self.connect()
            return
        # Receive. Should give ["report_all", data_string ,TIME_RECIEVED]

        string = ""
        for ele in msg[1]:
            string += ele
            if msg[1][len(msg[1]) - 1] != ele:
                string += ","
        try:
            self.data = json.loads(string)
            self.data['status'] = 3
            self.data['message'] = 'active'
        except UnicodeDecodeError:
            self.data['status'] = 3
            self.data['message'] = 'unicode decode error'
            self.logging.warning(self.data['message'])

    def get(self, value):
        # request status to polls
        if value == 'status':
            self.get_data()

        if value in self.data and self.data['status'] > 0:
            return self.data[value]
        else:
            if value == 'message':
                return "disconnected"
            if value == 'offsets':
                return ""
            else:
                return -1

    def set(self, value):
        if value[0] == 'offsets':
            self.c.send("set_offsets", *value[1])
