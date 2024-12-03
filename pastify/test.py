import urllib.parse
from app import Pastify
from utils import message
from dev import Watcher

app = Pastify()

@app.route(path="/", allowed_methods=["GET", "POST"])
def home(req, res):
    return res.send("<h1>home page '/' route</h1>")
    # res = "HTTP/1.1 200 OK\n\n<h1>home page '/' route ki esi ki te</h1>"
    # soc.sendall(res.encode())
    # soc.close()
@app.route(path="/xyz", allowed_methods=["GET"])
def xyz(req, res):
    res.send("<h1>ek galeech xyz route</h1>")


@app.route(path="/boy", allowed_methods=["GET"])
def xyz(req, res):
    res.send(f"<h1>galeech boy</h1>")


@app.route(path="/boy/:m/:q", allowed_methods=["GET"])
def xyz(req, res):
    res.send(f"<h1>galeech boy {req.params}</h1>")

@app.route(path="/hey/:page", allowed_methods=["GET"])
def xyz(req, res):
    j = req.params["page"]
    if j == "json":
        return res.json({"name": "tushar", "email": "aa"})
    
    elif j == "file":
        return res.fsend("./public/demo.txt")
    else:
        return res.send(f"<h1>{req.params["page"]} + {req.query}</h1>")
    
@app.route(path="/static/:file", allowed_methods=["GET"])
def xyz(req, res):
    file = req.params["file"]
    res.fsend("public/"+file)
    
    
@app.route(path="/te", allowed_methods=["GET"])
def xyz(req, res):
    res.render("sample.html", name="Tushar", pos=1, data='{"name":"tushar", "email": "hello"}')
    
watcher = Watcher(app, __file__)

watcher.listen(lambda data: message.cyan(data["message"]))