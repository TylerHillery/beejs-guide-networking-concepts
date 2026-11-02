import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument("port", nargs="?", type=int, default=28333)
args = parser.parse_args()

address = ("", args.port)

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)
s.listen()

while True:
    new_socket, addr = s.accept()
    print(new_socket)
    print(addr)

    request = b""
    while b"\r\n\r\n" not in request:
        d = new_socket.recv(4096)
        if not d:
            break
        request += d

    # TODO
    # modify the client to be able to send payloads
    # you'll need to be able to set `Content-Type` and `Content-Length` based on
    # payload 
    if b"\r\n\r\n" in request:
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 6\r\n"
            "Connecton: Close\r\n"
            "\r\n"
            "Hello!"
        )
        new_socket.sendall(response.encode("ISO-8859-1"))
        print("sent response")
    new_socket.close()