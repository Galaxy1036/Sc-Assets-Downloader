# -*- coding: utf-8 -*-
from threading import Thread 
from urllib.request import urlopen
from AssetsDecompressor import *
import os
import json
import ctypes
import sys

class Downloader(Thread):

	ThreadNumber    = 0
	StartPoint      = 0
	FilesCount      = 0
	FilesDownloaded = 0

	def __init__(self,AssetsUrl,FingerPrint,DownloadPath,SpecificFile,IncludeDecompression):
		Downloader.ThreadNumber   += 1
		Thread.__init__(self)
		self.AssetsUrl            = AssetsUrl
		self.FingerPrint          = FingerPrint
		self.DownloadPath         = DownloadPath
		self.SpecificFile         = SpecificFile
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

		if self.SpecificFile:
			for i in self.FingerPrint['files']:
				if i['file'].endswith(self.SpecificFile):
					Downloader.FilesCount += 1 / Info[1]
		else:
			Downloader.FilesCount = len(self.FingerPrint['files'])

		for i in range(Info[0],len(self.FingerPrint['files']),Info[1]):
			DirName = self.DownloadPath + '/' + MasterHash +'/'
			FileName = self.FingerPrint['files'][i]['file']
			FileUrl = self.AssetsUrl + '/' + MasterHash + '/' + FileName
			if self.SpecificFile:
				if FileName.endswith(self.SpecificFile):
					if self.IncludeDecompression:
						if FileName.endswith(('.csv','.sc')):
							self.downloadFile(FileUrl,DirName,FileName,True)

						else:
							self.downloadFile(FileUrl,DirName,FileName)

					else:
						self.downloadFile(FileUrl,DirName,FileName)

			else:
				if self.IncludeDecompression:
					if FileName.endswith(('.csv','.sc')):
						self.downloadFile(FileUrl,DirName,FileName,True)

					else:
						self.downloadFile(FileUrl,DirName,FileName)

				else:
					self.downloadFile(FileUrl,DirName,FileName)

	def downloadFile(self,FileUrl,DirName,FileName,decompress=False):

		FilePath = DirName + FileName
		if os.path.exists(FilePath):
			print('[*] {} was already downloaded'.format(FileUrl.split('/')[-1]))

		else:
			File = urlopen(FileUrl)
			print('[*] {} has been downloaded'.format(FileUrl.split('/')[-1]))
			os.makedirs(os.path.dirname(DirName + FileName), exist_ok=True)
			with open(DirName + FileName,'wb') as f:
				if decompress:
					f.write(Decompressor(File.read(),FileName))
					f.close()

				else:
					f.write(File.read())
					f.close()

		Downloader.FilesDownloaded += 1
		if os.name == "nt":
			ctypes.windll.kernel32.SetConsoleTitleW("Download [{}/{}]".format((Downloader.FilesDownloaded),round(Downloader.FilesCount)))

		else:
			sys.stdout.write("\x1b]2;Download [{}/{}]\x07".format((Downloader.FilesDownloaded),round(Downloader.FilesCount)))

	
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

	for i in range(ThreadCount):
		
		locals()['Thread{}'.format(i)].start()
