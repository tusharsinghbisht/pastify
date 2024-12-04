from app import Pastify
from utils import message
from dev import Watcher
from middleware import parseJSON
from routes import adminRouter

app = Pastify()

app.useStatic()
app.use(parseJSON)

app.useRouter(adminRouter)

@app.route(path="/", allowed_methods=["GET", "POST"])
def home(req, res):
    return res.send("<h1>home page '/' route</h1>")
    # res = "HTTP/1.1 200 OK\n\n<h1>home page '/' route ki esi ki te</h1>"
    # soc.sendall(res.encode())
    # soc.close()
@app.route(path="/xyz", allowed_methods=["GET"])
def xyz(req, res):
    res.send("<h1>ek galeech xyz route</h1>")


@app.route(path="/boy", allowed_methods=["GET"], middlewares=[lambda r,s: print("boy wala route")])
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
    
    
    
@app.route(path="/te", allowed_methods=["GET"])
def xyz(req, res):
    res.render("sample.html", name="Tushar", pos=1, data={"name":"tushar", "email": "hello"}, data2=[1,3,4])

    
    
@app.route(path="/head", allowed_methods=["GET"])
def xyz(req, res):
    res.setCookie("oo", "abc", 3600)
    res.send("ye headers testing ke liye hai")

    
    
@app.route(path="/red", allowed_methods=["GET"])
def xyz(req, res):
    res.redirect("/te")
    
@app.route(path="/submit", allowed_methods=["POST"])
def xyz(req, res):
    # print(req.body)
    res.send("form submitted")
    
    
watcher = Watcher(app, __file__)

watcher.listen(lambda data: message.cyan(data["message"]))