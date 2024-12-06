from pastify.app import Router

adminRouter = Router("/admin", middlewares=[lambda r,s: print("admin ka route")])

@adminRouter.route(path="/", allowed_methods=["GET"])
def xyz(req, res):
    res.send("<h1>ek galeech xyz route</h1>")

@adminRouter.route(path="/val/:xyz", allowed_methods=["GET"])
def xyz(req, res):
    res.send(f"<h1>admin ka params {req.params["xyz"]}</h1>")