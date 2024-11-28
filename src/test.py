from app import Pastify
from utils import message
from dev import Watcher
app = Pastify()

@app.route(path="/", allowed_methods=["GET"])
def home(soc):
    res = "HTTP/1.1 200 OK\n\n<h1>home page '/' route</h1>"
    soc.sendall(res.encode())
    soc.close()

@app.route(path="/xyz", allowed_methods=["GET"])
def xyz(soc):
    res = "HTTP/1.1 200 OK\n\n<h1>ek galeech xyz route</h1>"
    soc.sendall(res.encode())
    soc.close()

# app.route("/", ["GET"], home)
# app.route("/xyz", ["GET"], xyz)

watcher = Watcher(app)

watcher.listen(lambda data: message.cyan(data["message"]))