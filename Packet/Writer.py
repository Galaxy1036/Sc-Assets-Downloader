# -*- coding: utf-8 -*-


class Writer:

    def __init__(self):
        self.buffer = b''
        self.header = b''

    def putInt(self, data, length=4):
        self.buffer += data.to_bytes(length, 'big')

    def putString(self, data):
        self.putInt(len(data))
        self.buffer += data.encode('utf-8')

    def buildBuffer(self):
        self.header += self.Id.to_bytes(2, 'big')
        self.header += len(self.buffer).to_bytes(3, 'big')

        if hasattr(self, 'version'):
            self.header += self.version.to_bytes(2, 'big')

        else:
            self.header += (0).to_bytes(2, 'big')

        return self.header + self.buffer


def Write(Packet):
    Packet = Packet()
    Writer.__init__(Packet)
    Packet.process()
    return Packet.buildBuffer()
