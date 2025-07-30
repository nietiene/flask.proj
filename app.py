# flask is web framework used to build web application
# it can handle both frontend and backend
# it when you're using any frontend framework you can use it for backend only 

from flask import Flask, render_template, request, make_response 
# in this code Flask is main class to create web wapp
# render_template is function used to render html file from template folder

app = Flask(__name__)
# this it create flask app instance
# __name__ tells flask where to look for resources like template, static, files

@app.route('/')
# specifiy route

def home():
    return render_template("home.html")

@app.route("/user")
def greet():
    return render_template("home.html")



# forms(get input from users) we use flask's request to capture data
@app.route("/form", methods=["GET", "POST"])
# methods allow both GET and PODT http method
def index():
    # define index functio that will runs when user visited /form
    if request.method == "POST":
        # this check if user is already clicked on post buttom
        name = request.form["name"]
        # req.form takes value name like input type="name"
        return render_template("greeting.html", username = name)
        #  render greeting page with user's name 
    return render_template("form.html")
# this is default page when user visit page without submitting

# jinja2 is template engine used in flask it lets you insert Pythin logic int HTML using {{}} and {% %}
# on variables we use {{ variable }}

# on conditionals {% %}
# {% if age > 18 %}
#   <p>You are an adult</p>
# {% else: %}
#   <p><You are underage./p>

# on loops
# <ul>
#   {% for user in users %}
#     <li>{{ user }}</li>
#   {% endfor %}
# </ul>
# {# comments #}


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":
            return f"welcome {username}"
        else:
            return "Invalid username or password"
# if it is get request show login form 

    return render_template("login.html")


# cookie and session
# cookie small  piece of data stored on the client browser
#  we use make_response class which is used to create custom response object so you can use it in cookies

@app.route('/setcookie')
def set_cookie():
    res = make_response("Cookie is set")
    # this cookie will displayed if the cookie if already set
    res.set_cookie('username', 'Etiene')
    # this line set cookie 
    # username is cookie name
    # etiene is cookie value
    return res

@app.route('/getcookie')
def get_cookie():
    username = request.cookies.get('username')
    # request.cookie it store all cookies sends
    # .get("username") means give me value of cookie named username
    return f'cookie value is: {username}'


# import blueprint
from auth.routes import auth 
# from auth folder and routes file we import auth blueprint
# auth is folder, routes is file auth is blueprint

# register blueprint
app.register_blueprint(auth, url_prefix="/auth")
# this register the auth blueprint with your main flask app
# it tells flask to include all routes from this blueprint and prefix them with /auth


if __name__ == "__main__":
# only run if file is executed directly not imported
    app.run(debug=True)
    # start flsk development server
    # debut=True Enable auto-reloading no need to start the server for changes
