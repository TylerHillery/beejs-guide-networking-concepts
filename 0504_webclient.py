import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument("host")
parser.add_argument("port", nargs="?", type=int, default=80)
args = parser.parse_args()

address = (args.host, args.port)

request = f"GET / HTTP/1.1\r\nHost: {args.host}\r\nConnection: close\r\n\r\n"
request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {args.host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

s = socket.socket()
s.connect(address)
s.sendall(request.encode("ISO-8859-1"))

while True:
    # TODO
    # 1. modify the server to be able to extract and print the request method
    # 2. modify the server to extract and print a payload sent by the client
    d = s.recv(4096)
    if not d:
        break
    print(d.decode("ISO-8859-1"), end="")

s.close()