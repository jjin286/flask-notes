"""Flask app for notes app."""

import os

from flask import Flask, render_template, redirect, session, flash
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm, EditNoteForm
from models import connect_db, db, User, Note

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


#################################################### Log in/Log out/Register

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


@app.post('/logout')
def logout_user():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(AUTH_USER, None)

    return redirect("/")


############################################### Show user/Delete user


@app.get('/users/<username>')
def show_user(username):
    """Show user information"""

    if AUTH_USER not in session:
        flash("You must be logged in to view!")
        return redirect('/')
    if username != session[AUTH_USER]:
        flash(f"You are logged in as {session[AUTH_USER]}")

    form = CSRFProtectForm()

    user = User.query.get_or_404(session[AUTH_USER])

    return render_template('user_detail.html', user=user, form=form)


@app.post('/users/<username>/delete')
def delete_user(username):
    """Delete the user from database"""
#TODO: Save session[AUTH_USER] to variable
    if AUTH_USER not in session:
        flash("You must be logged in to view!")
        return redirect('/')
    if username != session[AUTH_USER]:
        # TODO: import Unauthorized
        flash(f"Logged in as {session[AUTH_USER]}. Cannot delete user {username}")
        return redirect(f'/users/{session[AUTH_USER]}')

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(AUTH_USER, None)
        user = User.query.get_or_404(session[AUTH_USER])
        notes = Note.query.filter_by(owner_username=session[AUTH_USER]).delete()
        db.session.delete(user)
        db.session.commit()

    return redirect('/')


############################################### Add note/Edit note/Delete note


@app.route('/users/<username>/notes/add', methods=['GET', 'POST'])
def add_note(username):
    """Show new note form and add to database"""

    if AUTH_USER not in session:
        flash("You must be logged in to view!")
        return redirect('/')

    if username != session[AUTH_USER]:
        #TODO: unauthorized
        flash("You can only create notes for yourself")
        return redirect(f'/users/{ session[AUTH_USER] }/notes/add')

    form = AddNoteForm()

    User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner_username=session[AUTH_USER])

        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{session[AUTH_USER]}')
    else:
        return render_template('add_note.html', form=form)


@app.route('/notes/<note_id>/update', methods=['GET', 'POST'])
def update_note(note_id):
    """Show edit note form and update the database"""

    if AUTH_USER not in session:
        flash("You must be logged in to view!")
        return redirect('/')

    note = Note.query.get_or_404(note_id)

# Don't need to go to user instance to get username, already have FK
    if note.user.username != session[AUTH_USER]:
        flash("You can only edit notes created by you")
        return redirect(f'/users/{session[AUTH_USER]}')

    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{session[AUTH_USER]}')

    else:
        return render_template('edit_note.html', form=form)


@app.post('/notes/<note_id>/delete')
def delete_note(note_id):
    """Delete note from database"""

    if AUTH_USER not in session:
        flash("You must be logged in to view!")
        return redirect('/')

    note = Note.query.get_or_404(note_id)

# 191
    if note.user.username != session[AUTH_USER]:
        flash("You can only delete notes created by you")
        return redirect(f'/users/{session[AUTH_USER]}')

    form = CSRFProtectForm()

    if form.validate_or_404():
        db.session.delete(note)
        db.session.commit()


    return redirect(f"/users/{session[AUTH_USER]}")







