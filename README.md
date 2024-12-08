# Pastify

**Pastify** is a simple minimalistic Python web framework inspired by Flask, built using the unix socket API. It aims to provide a lightweight, easy-to-understand alternative for learning the basics of web frameworks and HTTP handling. With Pastify, developers can define routes, handle HTTP requests, and send responses without relying on external web server dependencies.

---

## Features

- **Routing System**: Map URLs to Python functions, parses routes with params and query also
- **HTTP Request Parsing**: Handle headers, query parameters, and request bodies.
- **HTTP Response Generation**: Send custom headers, status codes, and response bodies.
- **Middleware Support**: Add functionality to requests and responses via middleware.
- **Custom Error Handling**: Handle errors with user-defined responses.
- **Static File Serving**: *Serve** static assets like HTML, CSS, and JavaScript files.
- **Template engine**: Supports basic templating and can render templates like Flask Jninja2

---

## Installation

Install the module to use it:

```bash
pip install pastify
```

## Working with pastify

#### Creating a simple web server

```python
from pastify.app import Pastify

app = Pastify()

# Defining the / route
@app.route("/", allowed_methods=["GET"])
def home(req, res):
    res.send("Hello, World!")

app.listen(lambda status, message: print(message))
```

#### Updating HOST and PORT

```python
app = Pastify('0.0.0.0', 3000)
```

#### Starting server in watch mode for development

```python
from pastify.app import Pastify
from pastify.dev import Watcher

app = Pastify()
@app.route("/", allowed_methods=["GET"])
def home(req, res):
    res.send("Running in watch mode....")


watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))
```

#### Defining more routes

```python
from pastify.app import Pastify
from pastify.dev import Watcher

app = Pastify()

@app.route("/", allowed_methods=["GET"])
def home(req, res):
    res.send("Home page....")

@app.route("/about", allowed_methods=["GET"])
def about(req, res):
    res.send("About page....")


@app.route("/blog", allowed_methods=["GET"])
def blog(req, res):
    res.send("Blog page....")


watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))

```

#### Serving static files

```python
from pastify.app import Pastify
from pastify.dev import Watcher

app = Pastify()

# binds all files of ./public directory to /static route
app.useStatic("./public", "/static") 

@app.route("/", allowed_methods=["GET"])
def home(req, res):
    res.send("Home page...")


watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))
```

#### Giving JSON response

```python
from pastify.app import Pastify
from pastify.dev import Watcher

app = Pastify()

@app.route("/user/getData", allowed_methods=["GET"])
def getUserData(req, res):
    ## dynamically fetch data from database ##

    # sending json response with res.json, while res.send helps sending text response
    res.json({
        "id": "31",
        "name": "Tushar",
        "age": 18,
        "college": "DTU"
    })

watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))


```

#### Middlewares : Global and route specific

```python
from pastify.app import Pastify
from pastify.dev import Watcher
from pastify.middleware import parseJSON

app = Pastify()

app.use(parseJSON) # Inbuilt middleware for parsing request body to JSONs

def global_middleware(req, res):
    print("global middlware") # printed before every route

app.use(global_middleware) # used to make a global middleware

@app.route("/", allowed_methods=["GET"])
def home(req, res):
    res.send("Home page....")

@app.route("/about", allowed_methods=["GET"])
def about(req, res):
    res.send("About page....")

def blog_middleware(req, res):
    print("blog middleware") # only prints /before blog route

@app.route("/blog", allowed_methods=["GET"], middlewares=[blog_middlewares])
def blog(req, res):
    res.send("Blog page....")


watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))

```

#### Route with params, query and body

```python
from pastify.app import Pastify
from pastify.dev import Watcher
from pastify.middleware import parseJSON

app = Pastify()

app.use(parseJSON) # parse req.body as json

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
    email = req.body.get("email")
    pw = req.body.get("pass")

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


watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))
```

#### Setting response status, headers and cookie

```python
from pastify.app import Pastify
from pastify.dev import Watcher

app = Pastify()

@app.route("/", allowed_methods=["GET"])
def home(req, res):
    res.status(201) # to set response status (by default: 200)
    res.message("NOT OK") # to set response message (by default: OK)
    res.setHeaders({ "X-Custom-Header": "a_Random_val" }) # to set/modify headers
    res.setCookie("a_cookie", "value_of_cookie", 3600) # to set/modify cookies

    res.send("<h1>Welcome to pastify!!!</h1>")

watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))
```

#### Sending files and redirects

```python
from pastify.app import Pastify
from pastify.dev import Watcher

app = Pastify()

@app.route("/get_text", allowed_methods=["GET"])
def getText(req, res):
   res.fsend("example.txt") # sends content from file `example.txt`

@app.route("/show_text", allowed_methods=["GET"])
def showText(req, res):
   res.redirect("/get_text") # `/show_text` redirects to `/get_text`


watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))


```

#### Rendering template

```python
from pastify.app import Pastify
from pastify.dev import Watcher

app = Pastify()

@app.route("/user/:userid/dashboard", allowed_methods=["GET"], 
middlewares=[lambda req, res: print("middleware for dashboard route")])
def dashboard(req, res):
    res.render("dashboard.html", user=req.params["userid"]) 
    # get's template from `templates` folder in current working 
    # directory and renders it with given value of user


watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))

```

```html
<!--templates/dashboard.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard for {{ user }}</title>
</head>
<body>
    <h1>Hii, {{ user }}</h1>
</body>
</html>
```

#### Defining sub-routes with same parent route

```python
from pastify.app import Pastify
from pastify.dev import Watcher

app = Pastify()

@app.route("/", allowed_methods=["GET"])
def home(req, res):
    res.send("Home page....")


from routes.pageRoutes import pageRouter

app.useRouter(pageRouter) # use page router
## more such routers can be added ##

watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))

```

```python
# routes/pages.py

# all routes defined with pageRouter are prefixed with /page

from pastify.app import Router

def page_middleware(req, res):
    print("middleware only for /page routes") # prints before every route prefixed with /page

pageRouter = Router("/page", middlewares=[page_middleware])


@pageRouter.route("/about", allowed_methods=["GET"]) # points to /page/about
def about(req, res):
    res.send("this is about page")

@pageRouter.route("/blog", allowed_methods=["GET"], 
middlewares=[lambda req, res: print("middlware for /page/blog route")]) # points to /page/about
def about(req, res):
    res.send("this is blog page")

```

---

That' covers all major feaures of **pastify**, that can help you to create your own web app :)

Thankyou,
Feel free to raise an issue and contacting me

- my website: [tusharr.xyz](https://tusharr.xyz/)
- email: [aabisht2006@gmail.com](mailto:aabisht2006@gmail.com)
