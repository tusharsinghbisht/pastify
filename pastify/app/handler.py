import socket
from urllib.parse import unquote
import json
from .error import InternalServerError, FileNotExist, TemplateError
import os
import mimetypes
import re

BASE_URI = "./pastify"
BASE_URI_TEMPLATE = "./pastify/templates"

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
        self.sent = False

    def status(self, code):
        self.status_code = code
    def message(self, message):
        self.status_message = message

    def getStatus(self):
        return f"{self.status_code} {self.status_message}"

    def send(self, text: str):
        self.socket.sendall(f'{self.req.http_version} {self.getStatus()}\nContent-type: text/html\n\n{text}'.encode())
        self.socket.close()
        self.sent = True

    def json(self, dic):
        try:
            json_res = json.dumps(dic)
            self.socket.sendall(f'{self.req.http_version} {self.getStatus()}\nContent-type: application/json\n\n{json_res}'.encode())
            self.socket.close()
            self.sent = True
        except TypeError:
            raise InternalServerError

    def fsend(self, fname):
        try:
            file_path = os.path.join(BASE_URI, fname)

            if not os.path.isfile(file_path):
                raise FileNotExist
            else:
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = "application/octet-stream"

                f = open(file_path, "rb")
                content = f.read()
                f.close()
                res = f"{self.req.http_version} {self.getStatus()}\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n"
                self.socket.sendall(res.encode()+content)
                self.socket.close()
                self.sent = True
        except OSError:
            raise InternalServerError
            
    def render(self, template, **context):

        try:
            file_path = os.path.join(BASE_URI_TEMPLATE, template)

            if not os.path.isfile(file_path):
                raise TemplateError("Template not found", 404)
            else:
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type != "text/html":
                    raise TemplateError("Invalid template type", 415)

                
                f = open(file_path, "r")
                content = f.read()
                f.close()

                print(re.finditer(r"\{\{\s*(.*?)\s*\}\}", content))
                def replacer(match):
                    var = match.group(1)  
                    return str(context.get(var, f"{{{{ {var} }}}}"))

                res = re.sub(r"\{\{\s*(.*?)\s*\}\}", replacer, content)
                # res = re.sub(r"\{\{\s*(.*?)\s*\}\}", lambda m: str(context.get(v:=m.group(1), f"{{{{ {v} }}}}")), content)


                res = f"{self.req.http_version} {self.getStatus()}\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n{res}"
                self.socket.sendall(res.encode())
                self.socket.close()
                self.sent = True
        except OSError:
            raise InternalServerError