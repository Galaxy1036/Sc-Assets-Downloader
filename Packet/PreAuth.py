# -*- coding: utf-8 -*-

from Packet.Writer import Writer


class PreAuth(Writer):

    def __init__(self):
        self.Id = 10100

    def process(self):
        self.putInt(1)
        self.putInt(17)
        self.putInt(3)
        self.putInt(0)
        self.putInt(1051)
        self.putString('')
        self.putInt(2)
        self.putInt(2)
