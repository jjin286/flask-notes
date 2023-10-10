"""Flask app for notes app."""

import os

from flask import Flask, render_template, redirect, session, flash
from forms import RegisterForm, LoginForm,  CSRFProtectForm
from models import connect_db, db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")

connect_db(app)

AUTH_USER = 'auth_user'

@app.get('/')
def redirect_to_register():
    """Redirect user to /register"""

    return redirect('/register')


##################################################### Log in/Register/Log out
@app.route('/register', methods=["GET", "POST"])
def register():
    """Show register form and handle new user submit"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        username_exists = User.query.filter_by(username=username).one_or_none()
        email_exists = User.query.filter_by(email=email).one_or_none()

        if username_exists:
            form.username.errors = ["Username already exists"]
        if email_exists:
            form.email.errors = ["Email already in use"]
        if (username_exists or email_exists):
            return render_template('register.html', form=form)

        user = User.register(
            username,
            password,
            email,
            first_name,
            last_name)

        db.session.add(user)
        db.session.commit()

        session[AUTH_USER] = user.username

        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Show login form and handle login"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            session[AUTH_USER] = user.username
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ["Incorrect name/password"]

    return render_template("login.html", form=form)


@app.get('/users/<username>')
def show_user(username):
    """Show user information"""
    form = CSRFProtectForm()
    if AUTH_USER not in session:
        flash("You must be logged in to view!")
        return redirect('/')



# TODO: move guard condition to top, line 97

    else:
        user = User.query.get_or_404(session[AUTH_USER])
        if username != session[AUTH_USER]:
            flash(f"You are logged in as {session[AUTH_USER]}")
        return render_template('user_detail.html', user=user, form=form)

#TODO: group common routes together
@app.post('/logout')
def logout_user():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(AUTH_USER, None)

    return redirect("/")