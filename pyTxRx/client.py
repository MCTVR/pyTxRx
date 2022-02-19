from os import path
import socket

host = "127.0.0.1"
port = 1145

filename = input("Input Filename: ")
filesize = path.getsize(filename)
SEP = "[SEP]"

if filesize >= 1000000000:
    FILE_BUFFER_SIZE = 16384
elif filesize >= 100000000 and filesize < 1000000000:
    FILE_BUFFER_SIZE = 4096
elif filesize >= 10000000 and filesize < 100000000:
    FILE_BUFFER_SIZE = 2048
else:
    FILE_BUFFER_SIZE = 1024

s = socket.socket()
s.connect((host, port))
s.send(f"<INFO>{filename}{SEP}{filesize}</INFO>".encode())

progress = 0
with open(filename, 'rb') as f:
    print("[+] File Sending...")
    while True:
        buffer = f.read(FILE_BUFFER_SIZE)
        if not buffer:
            print("[+] File Sent!")
            break
        s.sendall(buffer)

s.close()
