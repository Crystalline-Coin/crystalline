class Peer:
    def __init__(self, port, ip):
        self.port = port
        self.ip = ip

    def __str__(self):
        return "IP" + self.ip + " PORT:" + self.port
