from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user

# blueprint handles regular routes
main = Blueprint('main', __name__)

# index get route
@main.route('/')
def index():
 return render_template('index.html')

# help route | go here after logging in
@main.route('/help')
def help():
 # flash a message when the user logs in
 flash("please exercise caution when monitoring nests to ensure the safety of birds, nests and eggs.")
 return render_template('help.html')

