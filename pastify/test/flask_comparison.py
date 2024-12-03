from flask import Flask

app = Flask(__name__)

@app.route('/no-response')
def no_response():
    # No return value
    pass

if __name__ == '__main__':
    app.run(debug=True)
