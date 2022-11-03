
import socket
import os
SEPARATOR = "<SEPARATOR>"
# HOST = "127.0.0.1" 
HOST = "10.0.0.27"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
BUFFER_SIZE=4096
path=os.getcwd()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    value1_from_host=s.recv(1024)
    file_name=bytes.decode(value1_from_host)
    print(f"we recieved frm raspberry pi {file_name}")
    s.sendall(b"host is waiting for file size")
    value2_from_host=s.recv(1024)
    filesize=bytes.decode(value2_from_host)
    print(f"the file size is {filesize}")
    new_file=open(file_name,"w")
    s.sendall(b"host is waiting for file to be send ")
    print(filesize)
    while True:
            value3_from_host=s.recv(int(filesize))
            new_file.write(bytes.decode(value2_from_host))
            s.sendall(b"raspberry pi function protocol is complete")
   

  

