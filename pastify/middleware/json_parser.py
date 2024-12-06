from pastify.app.error import InternalServerError
from urllib.parse import parse_qs
import json

def parseJSON(req, res):
    '''Basic middleware for parsing request body to JSON format'''
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
            if req.headers.get("Content-Type", None) == (_:="application/json") or req.headers.get("Content-type", None) == _:
                req.json = json.loads(req.body)
            else:
                temp = {key: value[0] if len(value) == 1 else value for key, value in parse_qs(req.body).items()}
                
                if len(temp) != 0:
                    req.body = temp
            
    except Exception as e:
        print(e)
        print("Error in parsing body to JSON")
        raise InternalServerError("Error parsing json body")