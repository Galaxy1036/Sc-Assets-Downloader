# -*- coding: utf-8 -*-
from threading import Thread 
from urllib.request import urlopen
from AssetsDecompressor import *
import os
import json

class Downloader(Thread):

	ThreadNumber = 0
	StartPoint = 0

	def __init__(self,AssetsUrl,FingerPrint,DownloadPath,SpecificFile,IncludeDecompression):
		Downloader.ThreadNumber += 1
		Thread.__init__(self)
		self.AssetsUrl = AssetsUrl
		self.FingerPrint = FingerPrint
		self.DownloadPath = DownloadPath
		self.SpecificFile = SpecificFile
		self.IncludeDecompression = IncludeDecompression

	@classmethod
	def GetThreadNumber(cls):
		return cls.ThreadNumber

	@classmethod
	def GetStartPoint(cls):
		try:
			return cls.StartPoint
		finally:
			cls.StartPoint += 1

	def run(self):
		Info = self.GetStartPoint(),self.GetThreadNumber()
		MasterHash = self.FingerPrint['sha']

		for i in range(Info[0],len(self.FingerPrint['files']),Info[1]):
			DirName = self.DownloadPath + '/' + MasterHash +'/'
			FileName = self.FingerPrint['files'][i]['file']
			FileUrl = self.AssetsUrl + '/' + MasterHash + '/' + FileName
			if self.SpecificFile:
				if FileName.endswith(self.SpecificFile):
					if self.IncludeDecompression:
						if FileName.endswith(('.csv','.sc')):
							File = urlopen(FileUrl)
							print('[*] {} has been downloaded'.format(FileUrl.split('/')[-1]))
							os.makedirs(os.path.dirname(DirName + FileName), exist_ok=True)
							with open(DirName + FileName,'wb') as f:
								f.write(Decompressor(File.read(),FileName))
								f.close()

						else:
							File = urlopen(FileUrl)
							print('[*] {} has been downloaded'.format(FileUrl.split('/')[-1]))
							os.makedirs(os.path.dirname(DirName + FileName), exist_ok=True)
							with open(DirName + FileName,'wb') as f:
								f.write(File.read())
								f.close()

					else:

						File = urlopen(FileUrl)
						print('[*] {} has been downloaded'.format(FileUrl.split('/')[-1]))
						os.makedirs(os.path.dirname(DirName + FileName), exist_ok=True)
						with open(DirName + FileName,'wb') as f:
							f.write(File.read())
							f.close()						

			else:
				if self.IncludeDecompression:
					if FileName.endswith(('.csv','.sc')):
						File = urlopen(FileUrl)
						print('[*] {} has been downloaded'.format(FileUrl.split('/')[-1]))
						os.makedirs(os.path.dirname(DirName + FileName), exist_ok=True)
						with open(DirName + FileName,'wb') as f:
							f.write(Decompressor(File.read(),FileName))
							f.close()

					else:
						File = urlopen(FileUrl)
						print('[*] {} has been downloaded'.format(FileUrl.split('/')[-1]))
						os.makedirs(os.path.dirname(DirName + FileName), exist_ok=True)
						with open(DirName + FileName,'wb') as f:
							f.write(File.read())
							f.close()
				else:
					File = urlopen(FileUrl)
					print('[*] {} has been downloaded'.format(FileUrl.split('/')[-1]))
					os.makedirs(os.path.dirname(DirName + FileName), exist_ok=True)
					with open(DirName + FileName,'wb') as f:
						f.write(File.read())
						f.close()
					
def StartDownload(AssetsUrl,FingerPrint,SpecificFile=None,IncludeDecompression = None):
	if os.path.exists('config.json'):
		with open('config.json','r') as f:
			Config = json.load(f)
			ThreadCount = Config['ThreadNumber']
			DownloadPath = Config['DownloadPath']
	else:
		ThreadCount = 4
		DownloadPath = 'Download/'

	print('[*] Start download with {} threads'.format(ThreadCount))

	for i in range(ThreadCount):

		locals()['Thread{}'.format(i)] = Downloader(AssetsUrl,FingerPrint,DownloadPath,SpecificFile,IncludeDecompression)
		locals()['Thread{}'.format(i)].start()
