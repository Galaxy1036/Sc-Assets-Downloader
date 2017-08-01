# -*- coding: utf-8 -*-
#https://github.com/royale-proxy/cr-messages-python/blob/master/reader.py

from io import BufferedReader, BytesIO, SEEK_CUR
import zlib
from sys import byteorder


class CoCMessageReader(BufferedReader):

	def __init__(self,initial_bytes):
		super(CoCMessageReader, self).__init__(BytesIO(initial_bytes))

	def read_byte(self):
		return int.from_bytes(self.read(1), byteorder="big")

	def read_scid(self):
		hi = self.read_rrsint32()
		lo = 0
		if(hi):
			lo = self.read_rrsint32()
		return hi * 1000000 + lo

	def read_rrslong(self):
		hi = self.read_rrsint32().to_bytes(4, byteorder="big")
		lo = self.read_rrsint32().to_bytes(4, byteorder="big")
		return int.from_bytes(hi + lo, byteorder="big")

	def read_short(self, length=2):
		return int.from_bytes(self.read(length), byteorder="big")

	def read_int(self, length=4):
		return int.from_bytes(self.read(length), byteorder="big")

	def _read_varint(self, isRr):
		shift = 0
		result = 0
		while True:
			byte = self.read(1)
			if isRr and shift == 0:
				byte = self._sevenBitRotateLeft(byte)

			i = int.from_bytes(byte, byteorder="big")
			result |= (i & 0x7f) << shift
			shift += 7
			if not (i & 0x80):
				break
		return result

	def read_int32(self):
		return self._read_varint(False)

	def read_sint32(self):
		n = self._read_varint(False);
		return (((n) >> 1) ^ (-((n) & 1)))

	def read_rrsint32(self):
		n = self._read_varint(True)
		return (((n) >> 1) ^ (-((n) & 1)))

	def _sevenBitRotateLeft(self, byte):
		n = int.from_bytes(byte, byteorder='big')
		seventh = (n & 0x40) >> 6 # save 7th bit
		msb = (n & 0x80) >> 7 # save msb
		n = n << 1 # rotate to the left
		n = n & ~(0x181) # clear 8th and 1st bit and 9th if any
		n = n | (msb << 7) | (seventh) # insert msb and 6th back in
		return bytes([n])

	def read_long(self):
		return self.read_int(8)

	def read_string(self):
		length = self.read_int()
		if length == pow(2, 32) - 1:
			return b""
		else:
			try:
				decoded = self.read(length)
			except MemoryError:
				raise IndexError("String out of range.")
			else:
				return decoded.decode('utf-8')

	def read_zstring(self):
		length = int.from_bytes(self.read(4), byteorder="big")
		if length == pow(2, 32) - 1:
			return b""
		zlength = int.from_bytes(self.read(4), byteorder="little")
		try:
			decoded = zlib.decompress(self.read(length - 4), 15, zlength)
		except MemoryError:
			raise IndexError("String out of range.")
		except (ValueError, zlib.error) as e:
			raise IndexError("Decompress error: {}".format(e))
		else:
			return decoded

	def peek_int(self, length=4):
		return int.from_bytes(self.peek(length)[:length], byteorder="big")