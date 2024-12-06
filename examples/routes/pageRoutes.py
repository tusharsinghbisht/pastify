from pastify.app import Router

def page_middleware(req, res):
    print("middleware only for /page routes")

pageRouter = Router("/page", middlewares=[page_middleware])


@pageRouter.route("/about", allowed_methods=["GET"]) # points to /page/about
def about(req, res):
    res.send("this is about page")

@pageRouter.route("/blog", allowed_methods=["GET"], middlewares=[lambda req, res: print("middlware for /page/blog route")]) # points to /page/about
def about(req, res):
    res.send("this is blog page")