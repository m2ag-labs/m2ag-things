import zerorpc


class Indicator:

    def __init__(self, config, logging):
        self.logging = logging
        self.config = config
        self.c = zerorpc.Client()
        try:
            self.c.connect("tcp://127.0.0.1:4242")
            self.data = {'pattern': self.c.mode({"pattern": 0}), 'brightness': self.c.mode({"brightness": 10})}
        except:
            self.data = {'pattern': -1, 'brightness': -1}
            self.logging.error("m2ag indicator service is not available")

    # TODO: modify to query the service for the actual data
    def get(self, attr):
        return self.data[attr]

    # TODO: add other controls to this.
    def set(self, value):
        try:
            self.data[value[0]] = self.c.mode({value[0]: value[1]})
        except zerorpc.exceptions.LostRemote:
            self.logging.error("m2ag indicator service is not available")
