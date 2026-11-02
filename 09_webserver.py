import argparse
import socket
import urllib.parse
from pathlib import Path

ROOT_PATH = Path(".") 

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

    request = b""
    while b"\r\n\r\n" not in request:
        data = new_socket.recv(4096)
        if not data:
            break
        request += data

    if b"\r\n\r\n" in request:
        data_decoded = data.decode("ISO-8859-1")
        print(data_decoded)
        for line in data_decoded.split("\r\n"):
            parts = line.split(" ")
            if parts[0] in ["GET"]:
                method, path, proto = parts
                url = urllib.parse.urlparse(path)

            # TODO: not secure as someone could send ../ to escape the server root path
            # should add comparios to ensure the abs path request starts with the same abs as root
            file_path = ROOT_PATH / url.path.lstrip("/")
            try:
                # TODO: this should probalby be rb so we don't have to encode later on
                with open(file_path, "r") as fh:
                    file_data = fh.read()

                # TODO: the content type should be dynamic based on the extension requested
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(file_data.encode('ISO-8859-1'))}\r\n"
                    "Connecton: Close\r\n"
                    "\r\n"
                    f"{file_data}"
                )
            except FileNotFoundError:
                response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: 14\r\n"
                    "Connecton: Close\r\n"
                    "\r\n"
                    "File not found"
                )

        new_socket.sendall(response.encode("ISO-8859-1"))
        print("sent response")

    new_socket.close()
