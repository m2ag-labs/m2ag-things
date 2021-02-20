import zerorpc


class Indicator:

    def __init__(self, config, logging):
        self.logging = logging
        self.config = config
        self.c = zerorpc.Client()
        self.c.connect("tcp://127.0.0.1:4242")
        self.data = {"mode": 0}

    def get(self, prop):
        return self.data['mode']

    def set(self, value):
        self.data['mode'] = self.c.mode(value[1])
