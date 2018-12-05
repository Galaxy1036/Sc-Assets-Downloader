# -*- coding: utf-8 -*-

import os
import sys
import json
import ctypes

from threading import Thread
from urllib.request import urlopen

from AssetsDecompressor import Decompress


class Downloader(Thread):

    threadNumber    = 0
    startPoint      = 0
    filesCount      = 0
    filesDownloaded = 0

    def __init__(self, assetsUrl, fingerprint, downloadPath, specificFile, includeDecompression, overwrite):
        Downloader.threadNumber   += 1
        Thread.__init__(self)
        self.assetsUrl            = assetsUrl
        self.fingerprint          = fingerprint
        self.downloadPath         = downloadPath
        self.specificFile         = specificFile
        self.includeDecompression = includeDecompression
        self.overwrite            = overwrite

    @classmethod
    def GetThreadNumber(cls):
        return cls.threadNumber

    @classmethod
    def GetStartPoint(cls):
        try:
            return cls.startPoint

        finally:
            cls.startPoint += 1

    def run(self):
        info = self.GetStartPoint(), self.GetThreadNumber()
        masterHash = self.fingerprint['sha']

        if self.specificFile:
            for i in self.fingerprint['files']:
                if i['file'].endswith(self.specificFile):
                    Downloader.filesCount += 1 / info[1]

        else:
            Downloader.filesCount = len(self.fingerprint['files'])

        for i in range(info[0], len(self.fingerprint['files']), info[1]):

            dirName = self.downloadPath + '/' + masterHash + '/'
            fileName = self.fingerprint['files'][i]['file']
            fileUrl = self.assetsUrl + '/' + masterHash + '/' + fileName

            if self.specificFile:
                if fileName.endswith(self.specificFile):
                    self.downloadFile(fileUrl, dirName, fileName)

            else:
                self.downloadFile(fileUrl, dirName, fileName)

    def downloadFile(self, fileUrl, dirName, fileName):
        filePath = dirName + fileName

        if os.path.exists(filePath) and not self.overwrite:
            print('[*] {} was already downloaded'.format(fileUrl.split('/')[-1]))
            self.updateConsoleTitle()

        else:
            try:
                file = urlopen(fileUrl)

            except:
                print('[*] Error while downloading {}'.format(fileUrl.split('/')[-1]))

            print('[*] {} has been downloaded'.format(fileUrl.split('/')[-1]))
            os.makedirs(os.path.dirname(dirName + fileName), exist_ok=True)

            with open(dirName + fileName, 'wb') as f:
                if self.includeDecompression and fileName.endswith(('.csv', '.sc')):
                    f.write(Decompress(file.read(), fileName))
                    f.close()

                else:
                    f.write(file.read())
                    f.close()

            self.updateConsoleTitle()

    def updateConsoleTitle(self):
        Downloader.filesDownloaded += 1

        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW("Download [{}/{}] ({} %)".format((Downloader.filesDownloaded), round(Downloader.filesCount), round(Downloader.filesDownloaded / Downloader.filesCount * 100)))

        else:
            sys.stdout.write("\x1b]2;Download [{}/{}] ({} %)\x07".format((Downloader.filesDownloaded), round(Downloader.filesCount), round(Downloader.filesDownloaded / Downloader.filesCount * 100)))


def StartDownload(assetsUrl, fingerprint, args):
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
            threadCount = config['ThreadNumber']
            downloadPath = config['DownloadPath']

    else:
        threadCount = 4
        downloadPath = 'Download/'

    threadList = []

    print('[*] Start download with {} threads'.format(threadCount))

    for i in range(threadCount):
        threadList.append(Downloader(assetsUrl, fingerprint, downloadPath, tuple(args.specific), args.decompress, args.overwrite))

    for thread in threadList:
        thread.start()

    if args.fingerprint:
        if os.path.exists(downloadPath + '/' + fingerprint['sha'] + '/fingerprint.json') and not args.overwrite:
            print('[*] fingerprint.json already downloaded')

        else:
            downloadedFingerPrint = urlopen(assetsUrl + '/' + fingerprint['sha'] + '/fingerprint.json')
            os.makedirs(os.path.dirname(downloadPath + '/' + fingerprint['sha'] + '/fingerprint.json'), exist_ok=True)

            with open(downloadPath + '/' + fingerprint['sha'] + '/fingerprint.json', 'wb') as f:
                f.write(downloadedFingerPrint.read())
                f.close()

            print('[*] fingerprint.json has been downloaded')
