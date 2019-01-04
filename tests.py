#!/usr/bin/python3
# -*- coding: utf-8 -*-
from os import remove, path, mkdir, rmdir
from jewels import Jewels
import subprocess
import unittest

class TestJewels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # generate a given keyfile
        with open('test.key', 'w', encoding='utf-8') as f:
            f.write('OY5CnGzd0hGVymEew4AwTFttFckz2DHboWAuBM2qzGM=')

        # generate file to encrypt
        with open('source.txt', 'w', encoding='utf-8') as f:
            f.write('hello world\n')

        # generate folders
        if not path.exists('src.d'):
            mkdir('src.d')
        if not path.exists('dest.d'):
            mkdir('dest.d')

        # files to encrypt
        with open('src.d/source_01.txt', 'w', encoding='utf-8') as f:
            f.write('first file\n')
        with open('src.d/source_02.txt', 'w', encoding='utf-8') as f:
            f.write('second file\n')


    @classmethod
    def tearDownClass(cls):

        files_to_remove = (
            'test.key',
            'test_01.key',
            'source.txt',
            'source',
            'source.encrypted',
            path.join('src.d', 'source_01.txt'),
            path.join('src.d', 'source_02.txt'),
            path.join('src.d', 'source_01'),
            path.join('src.d', 'source_02'),
            path.join('dest.d', 'source_01'),
            path.join('dest.d', 'source_02')
        )

        for f in files_to_remove:
            if path.exists(f):
                remove(f)

        folders_to_remove = (
            'src.d',
            'dest.d'
        )
        for d in folders_to_remove:
            rmdir(d)


    def test_keyfile_generation(self):

        # generate keyfile
        bashCommand = "jewels-cli keygen test_01.key"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        expected = b'Key saved in "test_01.key". Please put this file in a safe folder.\n'

        self.assertEqual(output, expected)


    def test_simple_encryption(self):

        # default encryption
        bashCommand = 'jewels-cli encrypt source.txt test.key'

        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        expected = b'Encrypted "source.txt".\n'
        self.assertEqual(output, expected)

        jewel = Jewels('test.key')
        data = jewel.decrypt('source')

        self.assertEqual(data, 'hello world\n')


    def test_named_encryption(self):

        # default encryption
        bashCommand = 'jewels-cli encrypt source.txt test.key -o source.encrypted'

        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        expected = b'Encrypted "source.txt".\n'
        self.assertEqual(output, expected)

        jewel = Jewels('test.key')
        data = jewel.decrypt('source.encrypted')

        self.assertEqual(data, 'hello world\n')


    def test_recursive_encryption(self):

        # default encryption
        bashCommand = 'jewels-cli encrypt -r src.d test.key'

        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        expected = b'Encrypted "src.d/source_01.txt".\nEncrypted "src.d/source_02.txt".\n'
        self.assertEqual(output, expected)

        jewel = Jewels('test.key')
        data_01 = jewel.decrypt('src.d/source_01')
        data_02 = jewel.decrypt('src.d/source_02')

        self.assertEqual(data_01, 'first file\n')
        self.assertEqual(data_02, 'second file\n')


    def test_named_recursive_encryption(self):

        # default encryption
        bashCommand = 'jewels-cli encrypt -r src.d test.key -o dest.d'

        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        expected = b'Encrypted "src.d/source_01.txt".\nEncrypted "src.d/source_02.txt".\n'
        self.assertEqual(output, expected)

        jewel = Jewels('test.key')
        data_01 = jewel.decrypt('dest.d/source_01')
        data_02 = jewel.decrypt('dest.d/source_02')

        self.assertEqual(data_01, 'first file\n')
        self.assertEqual(data_02, 'second file\n')


if __name__ == '__main__':
    unittest.main()
