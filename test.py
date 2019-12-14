# Author: Orwa Watad
# 12.12.2019
# ex-checkpoint
# test dropbear ssh server
# test a new command -U, listen on port 53 for udp packets
# if the magic number is correct then it's opened a tcp port.

import time
import unittest
import client
import os

class MyTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		os.system("sudo killall -9 dropbear")
		os.system("sudo dropbear -U")
		os.system("sudo dropbear -Up 4444")

	def test_1_correct_magic_open_port_22(self):
		msg = client.main('', 53, 0xDEADBEEF, 22, "sudo netstat -tulpn")
		self.assertEqual(msg, "msg from server: The magic number is correct! -> The port opened successfully.")

	def test_2_correct_magic_not_open_port(self):
		msg = client.main('', 53, 0xDEADBEEF, 22, "")
		self.assertEqual(msg, "msg from server: The magic number is correct! -> The port is already open.")

	def test_3_correct_magic_open_port_2222(self):
		msg = client.main('', 53, 0xDEADBEEF, 2222, "")
		self.assertEqual(msg, "msg from server: The magic number is correct! -> The port opened successfully.")

	def test_4_wrong_magic(self):
		msg = client.main('', 53, 0xDDDDDDDD, 4444, "")
		self.assertEqual(msg, "msg from server: Wrong magic number! -> Didn't open a new port.")

	def test_5_correct_magic_open_port_4444(self):
		msg = client.main('', 53, 0xDEADBEEF, 4444, "")
		self.assertEqual(msg, "msg from server: The magic number is correct! -> The port opened successfully.")

	# ======================================

	def test_6_correct_magic_open_port_22(self):
		msg = client.main('', 4444, 0xDEADBEEF, 33, "")
		self.assertEqual(msg, "msg from server: The magic number is correct! -> The port opened successfully.")

	def test_7_correct_magic_not_open_port(self):
		msg = client.main('', 4444, 0xDEADBEEF, 33, "")
		self.assertEqual(msg, "msg from server: The magic number is correct! -> The port is already open.")

	def test_8_correct_magic_open_port_2222(self):
		msg = client.main('', 4444, 0xDEADBEEF, 2222, "")
		self.assertEqual(msg, "msg from server: The magic number is correct! -> The port is already open.")

	def test_9_wrong_magic(self):
		msg = client.main('', 4444, 0xDDDDDDDD, 8888, "")
		self.assertEqual(msg, "msg from server: Wrong magic number! -> Didn't open a new port.")

	def test_10_correct_magic_open_port_4444(self):
		msg = client.main('', 4444, 0xDEADBEEF, 8888, "")
		self.assertEqual(msg, "msg from server: The magic number is correct! -> The port opened successfully.")

	@classmethod
	def tearDownClass(cls):
		os.system("sudo killall -9 dropbear")


def main():
	unittest.main()

if __name__ == '__main__':
	main()
