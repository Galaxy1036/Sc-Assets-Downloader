# -*- coding: utf-8 -*-

import lzma


def Decompress(file, filename):

    decompressor = lzma.LZMADecompressor()

    if filename.endswith('.csv'):  # CSV decompression
        data = file[0:8] + (b'\x00' * 4) + file[8:]

        try:
            decompressed = decompressor.decompress(data)
            print('[*] {} succesfully decompressed'.format(filename.split('/')[-1]))

        except lzma.LZMAError:
            decompressed = file
            print("[*] File can't be decompressed")

        except Exception as exception:
            decompressed = file
            print('[*] Unknowed error happened while decompression ({})'.format(exception.__class__.__name__))

        return decompressed

    if filename.endswith('.sc'):  # SC decompression (only lzma :/)
        data = file[26:35] + (b'\x00' * 4) + file[35:]

        try:
            decompressed = decompressor.decompress(data)
            print('[*] {} succesfully decompressed'.format(filename.split('/')[-1]))

        except lzma.LZMAError:
            decompressed = file
            print("[*] File can't be decompressed")

        except Exception as exception:
            decompressed = file
            print('[*] Unknowed error happened while decompression ({})'.format(exception.__class__.__name__))

        return decompressed
