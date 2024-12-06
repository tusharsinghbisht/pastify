from pastify.app import Pastify

app = Pastify()

@app.route("/", allowed_methods=["GET"])
def home(req, res):
    res.send("Hello, World!")

app.listen(lambda status, message: print(message))