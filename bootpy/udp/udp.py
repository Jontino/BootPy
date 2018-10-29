import threading
import socket
from..models import Relay

UDP_IP = "0.0.0.0"
# UDP_IP = "localhost"
UDP_PORT = 5005


class UdpServer:
    def __init__(self, ip_address, port):
        self.ip_adddress = ip_address
        self.port = port
        self._listener_thread = threading.Thread(target=worker, args=(self.ip_adddress, self.port))
        self._listener_thread.start()


def worker(ip_address, port):
    print(' * UDP listener thread started on {}:{}'.format(ip_address, port))
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((ip_address, port))

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        ip, port = addr
        print('Requested by:', addr)

        action = data.decode().split('#')[0].lower()
        parameters = data.decode().split('#')[1:]

        error = False
        errorCode = 0;

        if action == 'reboot':
            print("Action: reboot")

            if len(parameters) > 0:
                port = int(parameters[0])
                print("Parameter: %s" % port)
                Relay.reboot(port + 1)
            else:
                error = True
                errorCode = 2

        else:
            error = True
            errorCode = 1

        result = str.encode("OK")
        if error:
            result = str.encode("Error#%s" % errorCode)

        sock.sendto(result, addr)
        print('Reply to:', addr)
        print(result.decode())

