# routing means mapping url to a python function when user visits URL flask runs the fucntion and return something like htmpl pages

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to homepage"

@app.route("/about")
def about():
    return "this is about page"

@app.route("/user/<username>")
def greet_user(username):
    return f"Hello {username}"


if __name__ == "__main__":
    app.run(debug=True)