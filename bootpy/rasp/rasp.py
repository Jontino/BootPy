import threading
from bootpy.rasp.led import LED

class Rasp:
    _relays = []

    def configure_relays(self, relays):
        for relay in relays:
            self._relays.append(LED(relay.gpio))

    def reboot(self, interval, relay_id, event_id, callback):
        relay_index = relay_id - 1
        if self._relays[relay_index].is_lit is False:
            self.power_on(relay_index)
            timer = threading.Timer(interval, self.power_off, [callback, event_id, relay_id])
            timer.start()

    def power_on(self, relay_id):
        relay_index = relay_id - 1
        if relay_index < len(self._relays):
            self._relays[relay_index].on()
        else:
            print("power_on FAILED - Out of Index")

    def power_off(self, *args):
        args_relay_id = args[2]
        relay_index = args_relay_id - 1
        if relay_index < len(self._relays):
            self._relays[relay_index].off()
            args[0](args[1])
        else:
            print("power_off FAILED - Out of Index")


