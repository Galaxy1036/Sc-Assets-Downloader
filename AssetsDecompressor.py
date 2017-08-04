# -*- coding: utf-8 -*-
import lzma

def Decompressor(File,Filename):

	Decompressor = lzma.LZMADecompressor()

	if Filename.endswith('.csv'): #CSV decompression

		Data = File[0:8] + (b'\x00' * 4) + File[8:]

		try:
			Decompressed = Decompressor.decompress(Data)
			print('[*] {} succesfully decompressed'.format(Filename.split('/')[-1]))
		except:
			Decompressed = File
			print("[*] File can't be decompressed")

		return Decompressed

	if Filename.endswith('.sc'): #SC decompression (only lzma :/)

		NoHeader = File[26:]

		Data = NoHeader[0:9] + (b'\x00' * 4) + NoHeader[9:]

		try:
			Decompressed = Decompressor.decompress(Data)
			print('[*] {} succesfully decompressed'.format(Filename.split('/')[-1]))
		except:
			Decompressed = File
			print("[*] File can't be decompressed")

		return Decompressed
