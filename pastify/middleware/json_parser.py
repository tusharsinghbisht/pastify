from app.error import InternalServerError
import json
from urllib.parse import parse_qs
from email.parser import Parser

def parseJSON(req, res):
    try:
        if req.body.strip() != "":
            # seprator = req.body.split("\r\n")[0]
            # if seprator.startswith("--------"): # handling multipart/form-data body
            #     parts = req.body.split(seprator)[1:-1]
            #     for part in parts:
            #         print(part)
            #         part = part.strip()
            #         headers, body = part.split("\r\n\r\n", 1)
            #         print(headers, body)
            #         # headers = Parser().parsestr(headers.decode("utf-8"))
            #         # content_disposition = headers.get("Content-Disposition", "")
           
            req.body = {key: value[0] if len(value) == 1 else value for key, value in parse_qs(req.body).items()}
            
    except Exception as e:
        print(e)
        print("Error in parsing body to JSON")
        raise InternalServerError("Error parsing json body")