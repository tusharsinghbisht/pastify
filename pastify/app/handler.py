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
        data_split = self.data.split("\r\n")
        self.headers = data_split[0:data_split.index('')]
        self.method, self.url, self.http_version = self.headers[0].split()
        self.url = unquote(self.url)
        self.base_url = self.url.split("?")[0]

        self.headers = self.headers[1:]
        self.headers = { x[:(_:=x.find(':'))].strip(): x[_+1:].strip() for x in self.headers if x.strip() != "" } 
        self.host = ""
        self.user_agent = ""
        self.cookies = ""

        if "Host" in self.headers:
            self.host = self.headers["Host"]
        if "User-Agent" in self.headers:
            self.user_agent = self.headers["User-Agent"]
        if "Cookie" in self.headers:
            self.cookies = { c[:(_:=c.find("="))].strip(): c[_+1:].strip() for c in self.headers["Cookie"].split(";") } 

        self.body = "\r\n".join(data_split[data_split.index('')+1:])

        self.query = { x[:x.find("=")]:x[x.find("=")+1:] for x in self.url[1:].split('?') if "=" in x and x.strip() != ""}
        
        self.params = {}


    

class Response:
    def __init__(self, req: Request):
        self.socket = req.socket
        self.req = req
        self.status_code = 200
        self.status_message = "OK"
        self.sent = False
        self.headers = {
            "Content-Type": "text/html; charset=UTF-8"
        }
        self.cookies = {}

    def status(self, code):
        self.status_code = code
    def message(self, message):
        self.status_message = message

    def setHeaders(self, hdrs):
        if isinstance(hdrs, dict):
            for k, v in hdrs.items():
                self.headers[k] = v
        else:
            raise InternalServerError("Invalid values for headers")
        
    def setCookie(self, key, value, max_age, path="/", http_only=True, secure=False, samesite="Strict"):
        http_only_text = "httponly;" if http_only else ""
        secure_text = "secure;" if secure else ""
        self.headers["Set-Cookie"] = f"{key}={value}; Max-Age={max_age}; path={path}; {http_only_text} {secure_text} SameSite={samesite}"

    def getStatus(self):
        return f"{self.status_code} {self.status_message}"
    
    def getHeaders(self):
        headers_str = ""
        for k, v in self.headers.items():
            headers_str += f"{k}: {v}\n"
        return headers_str

    def send(self, text: str):
        self.setHeaders({ "Content-Length": len(text) })
        self.socket.sendall(f'{self.req.http_version} {self.getStatus()}\n{self.getHeaders()}\n{text}'.encode())
        self.socket.close()
        self.sent = True

    def json(self, dic):
        try:
            json_res = json.dumps(dic)
            self.setHeaders({ "Content-Type": "application/json", "Content-Length": len(json_res) })
            self.socket.sendall(f'{self.req.http_version} {self.getStatus()}\n{self.getHeaders()}\n{json_res}'.encode())
            self.socket.close()
            self.sent = True
        except TypeError:
            raise InternalServerError("Invalid JSON response")

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
                self.setHeaders({ "Content-Type": content_type, "Content-Length": len(content) })
                res = f"{self.req.http_version} {self.getStatus()}\r\n{self.getHeaders()}\r\n"
                self.socket.sendall(res.encode()+content)
                self.socket.close()
                self.sent = True
        except OSError:
            raise InternalServerError
        
    def redirect(self, url):
        self.setHeaders({ "Location": url })
        self.status(302)
        self.message("Found")
        self.send(f"Redirecting too... {url}")
            
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

                def replacer(match):
                    var = match.group(1)
                    return str(context.get(var, f"{{{{ {var} }}}}"))

                res = re.sub(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}", replacer, content)

                res = f"{self.req.http_version} {self.getStatus()}\r\nContent-Type: {content_type}\r\nContent-Length: {len(res)}\r\n\r\n{res}"
                self.socket.sendall(res.encode())
                self.socket.close()
                self.sent = True
        except OSError:
            raise InternalServerError