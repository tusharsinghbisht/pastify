import urllib.parse
import urllib.parse
from app import Pastify
from utils import message
from dev import Watcher
app = Pastify()

@app.route(path="/", allowed_methods=["GET"])
def home(req, res):
    res.send("<h1>home page '/' route</h1>")
    # res = "HTTP/1.1 200 OK\n\n<h1>home page '/' route ki esi ki te</h1>"
    # soc.sendall(res.encode())
    # soc.close()

@app.route(path="/xyz", allowed_methods=["GET"])
def xyz(req, res):
    res.send("<h1>ek galeech xyz route</h1>")


@app.route(path="/boy/:id", allowed_methods=["GET"])
def xyz(req, res):
    print(req.params)
    res.send(f"<h1>galeech boy {req.params["id"]}</h1>")

watcher = Watcher(app, __file__)

watcher.listen(lambda data: message.cyan(data["message"]))