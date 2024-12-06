from pastify.app import Pastify, Request, Response
from pastify.dev import Watcher
from pastify.middleware import parseJSON

app = Pastify()

app.useStatic("./public", "/static") # binds all files of ./public directory to /static route

app.use(parseJSON) # used to parse request body as JSON

def global_middleware(req, res):
    print("global middlware") # printed before every route

app.use(global_middleware) # used to make a global middleware

@app.route("/", allowed_methods=["GET"])
def home(req: Request, res: Response):

    res.status(201) # to set response status (by default: 200)
    res.message("NOT OK") # to set response message (by default: OK)
    res.setHeaders({ "X-Custom-Header": "a_Random_val" }) # to set/modify headers
    res.setCookie("a_cookie", "value_of_cookie", 3600) # to set/modify cookies

    res.send("<h1>Welcome to pastify!!!</h1>")

@app.route("/user/:id", allowed_methods=["GET"])
def user(req, res):
    res.send("this is user with id " + req.params["id"])


@app.route("/user/:id/getData", allowed_methods=["GET"])
def getUserData(req, res):
    ## dynamically fetch data from database ##
    res.json({
        "id": req.params.get("id"),
        "name": "Tushar",
        "age": 18,
        "college": "DTU"
    })

@app.route("/login", allowed_methods=["GET"])
def login(req, res):
    email = req.boy.get("email")
    pw = req.boy.get("pass")

    ## login in with email and pass (... add logic) ##

    res.json({
        "message": "login done"
    })

@app.route("/search", allowed_methods=["GET"])
def search(req, res):
    query = req.query.get("query") # if url is like this /search?query=xyz
    ## perform some database opertion to get results from query ##
    res.json({
        "query": query,
        "results": ["item1", "item2", "item3"] # results of search query
    })

@app.route("/get_text", allowed_methods=["GET"])
def getText(req, res):
   res.fsend("example.txt") # sends content from file `example.txt`

@app.route("/show_text", allowed_methods=["GET"])
def showText(req, res):
   res.redirect("/get_text") # `/show_text` redirects to `/get_text`

@app.route("/user/:userid/dashboard", allowed_methods=["GET"], middlewares=[lambda req, res: print("middleware for dashboard route")])
def dashboard(req, res):
    res.render("dashboard.html", user=req.params["userid"]) 
    # get's template from `template` folder in current working directory and renders it with given value of user

from routes.pageRoutes import pageRouter

app.useRouter(pageRouter) # use page router


watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))