from Crypto.Cipher import AES
import socket
import binascii
import os

HOST = '0.0.0.0'
PORT = 1337
DATA_FILE_PATH = "../session_data.txt"

key = binascii.unhexlify('602a534498e3ece978c615a50c4a266b28e2e630777a83ba55eb0982aa7dbfd3')

def decrypt_and_check(data):
	data = binascii.unhexlify(data)
	nonce, tag = data[:12], data[-16:]
	#print("[*] Nonce = {} ; tag = {}".format(binascii.hexlify(nonce), binascii.hexlify(tag)))
	cipher = AES.new(key, AES.MODE_GCM, nonce)
	return cipher.decrypt_and_verify(data[12:-16], tag)

def save(data):
	try:
		with open(DATA_FILE_PATH, "w+") as file:
			decoded_data = data.decode() #'{}'.format(data)
			file.write(decoded_data)
			file.flush()
			# print(decoded_data)
	except Exception as e:
		print("Failed to create file")
		print("Error:", e)
	os.system("python3 insert_data.py --source_file {}".format(DATA_FILE_PATH))

#data = binascii.unhexlify('9012a33bfb0a51dec4f96404cdd7300ec6afca1fa0d6679a7c036652d014a38faf909e9c44d08dffac121aa85d48b7256fa74542e2545e27dc070adfc03af26f2a32f50c2c311d5c91ff6de2ca3b4347da70669575c9b198f4')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((HOST, PORT))
	sock.listen()
	print("[+] Listening on {}:{}".format(HOST, PORT))
	while True:
		conn, addr = sock.accept()
		with conn:
			print('Connected by {}'.format(addr))
			data = b''
			while True:
				byte = conn.recv(1)
				if not byte:
					break
				data += byte
				if data[-1] == 0xa:
					break
			# print('Received', repr(data))
			try:
				data = decrypt_and_check(data.strip())
				# print(data)
				print("[*] Received {} bytes".format(len(data)))
				save(data)
			except ValueError:
				print("[*] Mac Check Failed")
	
