class LED:

    def __init__(self, number):
        self.gpio = number

    @property
    def is_lit(self):
        return False

    def on(self):
        print(' * GPIO:{0} => ON'.format(self.gpio))

    def off(self):
        print(' * GPIO:{0} => OFF'.format(self.gpio))