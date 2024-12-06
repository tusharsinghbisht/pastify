from pastify.app import Pastify
from pastify.dev import Watcher

app = Pastify()
@app.route("/", allowed_methods=["GET"])
def home(req, res):
    res.send("Running in watch mode....")


watcher = Watcher(app, __file__)
watcher.listen(lambda status, message: print(message))