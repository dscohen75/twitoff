"""
Minimal example, Flask web application
"""


from flask import Flask
app = Flask(__name__)  # __name__ gets populated with the file name of this file

@app.route("/")  # Listens for requests and sends responses
def hello():
    return "Hello World!"