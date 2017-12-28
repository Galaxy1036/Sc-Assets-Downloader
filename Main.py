# -*- coding: utf-8 -*-

from Packet.Writer import *
from Packet.Reader import * 
from Packet.PreAuth import *
from Downloader import *
import socket
import ctypes
import os
import argparse
import json
import sys

def recvall(sock,size):
	data = []
	while size > 0:
		sock.settimeout(5.0)
		s = sock.recv(size)
		sock.settimeout(None)
		if not s: raise EOFError
		data.append(s)
		size -= len(s)
	return b''.join(data)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Download assets from official servers')
	parser.add_argument('-s', help='Download only files with specified extension', type=str, nargs='+')
	parser.add_argument('-d', help='Decompress Csv and .sc files (tex.sc included)', action='store_true')
	args = parser.parse_args()

	if os.name == "nt":
		ctypes.windll.kernel32.SetConsoleTitleW("Starting download")

	else:
		sys.stdout.write("\x1b]2;Starting download\x07")

	s = socket.socket()
	s.connect(('game.clashroyaleapp.com',9339))
	s.send(Write(PreAuth))

	Header = s.recv(7)
	size = int.from_bytes(Header[2:5],'big')
	print('[*] Receiving {}'.format(int.from_bytes(Header[:2],'big')))
	data = recvall(s,size)
	Reader = CoCMessageReader(data)
	if Reader.read_rrsint32() == 7:
		print('[*] FingerPrint has been received')
	else:
		print('[*] PreAuth packet is outdated , please get the latest one on GaLaXy1036 Github !')
		sys.exit()

	FingerPrint = Reader.read_string()
	Reader.read_string()#null
	Reader.read_string()#null
	Reader.read_string()#null
	Reader.read_short() #Apparently vInt + Byte 
	Reader.read_string()#null
	Reader.read_byte() #Apparently vInt
	Reader.read_string()#Event Assets Url
	AssetsUrl = Reader.read_string()
	
	Json = json.loads(FingerPrint)
	print('[INFO] Version = {}, MasterHash = {}'.format(Json['version'],Json['sha']))
	if args.s:	
		StartDownload(AssetsUrl,Json,tuple(args.s),args.d)
	else:
		StartDownload(AssetsUrl,Json,IncludeDecompression= args.d)

