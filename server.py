
from flask import Flask, request
app = Flask(__name__)


@app.route("/get")
def hello():
    return request.args.get('num', '')

