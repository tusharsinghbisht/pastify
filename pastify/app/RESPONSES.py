'''
Basic Default templates for some particular type of responses
'''


INTERNAL_SERVER_ERROR_PAGE = """
<html><head><title>500 Internal Server Error</title></head><body><h1>500 Internal Server Error</h1><p>Oops! Something went wrong on our server.</p></body></html>
"""

METHOD_NOT_ALLOWED_PAGE = """
<html><head><title>405 Method Not Allowed</title></head><body><h1>405 Method Not Allowed</h1><p>The method you used is not allowed for this resource.</p></body></html>
"""

NOT_FOUND_PAGE = """
<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1><p>The page or file you are looking for does not exist.</p></body></html>
"""

TEMPLATE_ERROR_PAGE = lambda e: f"""
<html><head><title>Template Error</title></head><body><h1>Template Error</h1><p>{e}</p></body></html>
"""
