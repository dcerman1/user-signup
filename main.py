from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/welcome", methods=['POST'])
def welcome():
    if len(request.form['username']) < 3 or len(request.form['username']) > 20:
        username_error = "Username must be between 3 and 20 characters."
        username = request.form['username']
        template = jinja_env.get_template('signup.html')
        email = request.form['email']
        return template.render(username_error=username_error, username=username, email=email)
    
    if " " in request.form['username']:
        username_error = "Spaces are not permitted in usernames"
        username = request.form['username']
        email = request.form['email']
        template = jinja_env.get_template('signup.html')
        return template.render(username_error=username_error, username=username, email=email)

    if request.form['password'] != request.form['verify']:
        password_error = "Passwords Do Not Match"
        username = request.form['username']
        email = request.form['email']
        template = jinja_env.get_template('signup.html')
        return template.render(password_error = password_error, username=username, email=email)
    
    if len(request.form['password']) < 8:
        username = request.form['username']
        password_error = "Password must be longer than 8 characters"
        email = request.form['email']
        template = jinja_env.get_template('signup.html')
        return template.render(password_error = password_error, username=username, email=email)

    if " " in request.form['password']:
        password_error = "Spaces are not permitted in passwords."
        username = request.form['username']
        email = request.form['email']
        template = jinja_env.get_template('signup.html')
        return template.render(password_error=password_error, username=username, email=email)

    if request.form['email']:
        if len(request.form['email']) > 0 and len(request.form['email']) < 3 or len(request.form['email']) > 20:
            username = request.form['username']
            email_error = "Email must be between 3 and 20 characters."
            email = request.form['email']
            template = jinja_env.get_template('signup.html')
            return template.render(email_error=email_error, email=email, username=username)

        if "@" not in request.form['email'] or "." not in request.form['email']:
            username = request.form['username']
            email_error = "Email must not contain spaces and must contain an @ and a ."
            email = request.form['email']
            template = jinja_env.get_template('signup.html')
            return template.render(email_error=email_error, email=email, username=username)
       
    
    username = request.form['username']
    template = jinja_env.get_template('welcome.html')
    return template.render(name=username)
  

@app.route('/')
def index():
    template = jinja_env.get_template('signup.html')
    return template.render()

app.run()