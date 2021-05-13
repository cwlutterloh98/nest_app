from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# models for user
from .models import Users
from . import db

# blueprint handles regular routes
auth = Blueprint('auth', __name__)

# sign-in get route
@auth.route('/sign-in')
def signIn ():
    return render_template('sign-in.html')

# sign in post route
@auth.route('/sign-in', methods=['POST'])
def signIn_post():
 # get all fields from the request
 username = request.form.get('username')
 password = request.form.get('password')

 remember = True if request.form.get('remember') else False
 user = Users.query.filter_by(user=username).first()
 # check if the user actually exists
 # take the user-supplied password, hash it, and compare it to the hashed password in the

 if not user or not check_password_hash(user.password, password):
  flash('Please check your login details and try again.')
  return redirect(url_for('auth.signIn'))  # if the user doesn't exist or password is wr

 login_user(user, remember=remember)
 # if the above check passes, then we know the user has the right credentials
 return redirect(url_for('main.help'))


# this was used to help troubleshoot my work could reuse if need more users
@auth.route('/sign-up')
def signUp ():
 return render_template('sign-up.html')

@auth.route('/sign-up', methods=['POST'])
def signup_post():
    # get all fields from the request
    username = request.form.get('username')
    password = request.form.get('password')

    # find the user by email to check if it exists
    user = Users.query.filter_by(user=username).first()
    if user:
        flash('Username already exists')
        return redirect(url_for('auth.signUp'))
   # create a new user with the form data. Hash the password so the plaintext version isn't
    new_user = Users(user=username,
                    password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=12))
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.signIn'))

# handles get route for logout
@auth.route('/logout')
def logout():
    # flask login function logs a user out.
    logout_user()
    # redirect to index.html
    return redirect(url_for('main.index'))