from flask import Blueprint

# create blueprint
auth = Blueprint('auth', __name__)
# it creates blueprint named auth
# and then __name__ is help flask to know file location

# define routes
@auth.route('/login')
def login():
    return "<h2>Login page</h2>"

@auth.route('/register')
def register():
    return "<h2>Register Page</h2>"
