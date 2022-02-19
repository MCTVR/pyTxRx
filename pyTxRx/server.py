from os import path
import socket
from time import perf_counter_ns

host = "0.0.0.0"
port = 6969

SEPARATOR = "<SEPARATOR>"
INFO_BUFFER_SIZE = 1024
SEP = "[SEP]"

s = socket.socket()
s.bind((host, port))
s.listen(5)

client, addr = s.accept()

fileinfo = client.recv(INFO_BUFFER_SIZE).decode("unicode_escape")

idx1 = fileinfo.index("<INFO>")
idx2 = fileinfo.index("</INFO>")
res = ""
for idx in range(idx1 + len("<INFO>"), idx2):
    res = res + fileinfo[idx]

filename = res.split(SEP)[0]
filesize = int(res.split(SEP)[1])

if filesize >= 1000000000:
    FILE_BUFFER_SIZE = 16384
elif filesize >= 100000000 and filesize < 1000000000:
    FILE_BUFFER_SIZE = 4096
elif filesize >= 10000000 and filesize < 100000000:
    FILE_BUFFER_SIZE = 2048
else:
    FILE_BUFFER_SIZE = 1024

filename = path.basename(filename)

with open(f"./recv/{filename}", "wb+") as f:
    time_start = perf_counter_ns()
    print('[+] File Receiving:', filename)
    while True:
        data = client.recv(FILE_BUFFER_SIZE)
        if not data:
            time_end = perf_counter_ns()
            print('[+] File Received:', filename, "(" + str(path.getsize(f"./recv/{filename}")/10000) + 'KB)')
            print('[+] File Trasmitted In:', ("{:.3f}".format((time_end - time_start)/1000000000) + 's'), "(" + "{:.3f}".format((filesize / 1000000) / ((time_end - time_start)/1000000000)), "MB/s)")
            break
        f.write(data)

f.close()

client.close()

s.close()