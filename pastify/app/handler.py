import socket
from urllib.parse import unquote

class Request:
    def __init__(self, socket: socket.socket):
        self.socket = socket
        self.data = socket.recv(1500).decode()
        self.headers = self.data.split("\n")
        self.method, self.url, self.http_version = self.headers[0].split()
        
        self.url = unquote(self.url)
        self.base_url = self.url.split("?")[0]

        self.headers = self.headers[1:]
        self.headers = { x[:x.find(':')]: x[x.find(":")+2:] for x in self.headers if x.strip() != "" } 

        self.host = self.headers["Host"]
        self.user_agent = self.headers["User-Agent"]

        self.body = self.data.split("\r\n")[-1]

        self.query = { x[:x.find("=")]:x[x.find("=")+1:] for x in self.url[1:].split('?') if "=" in x and x.strip() != ""}
        
        self.params = {}


    

class Response:
    def __init__(self, req: Request):
        self.socket = req.socket
        self.req = req
        self.status_code = 200
        self.status_message = "OK"

    def status(self, code):
        self.status_code = code
    def message(self, message):
        self.status_message = message

    def send(self, text: str):
        self.socket.sendall(f'{self.req.http_version} {self.status_code} {self.status_message}\n\n{text}'.encode())
        self.socket.close()