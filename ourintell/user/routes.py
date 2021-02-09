from flask import request, Blueprint, jsonify, render_template, url_for, flash, redirect
from flask_login import current_user, login_user, logout_user

from ourintell import db,  bcrypt
from ourintell.user.forms import LoginForm, RegistrationForm
from ourintell.models import User


from sqlalchemy import exc

import json 
from hashlib import sha256

user = Blueprint('user',__name__)

@user.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('intell.getEvents'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('user.login'))
    return render_template("register.html", form = form)

@user.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('intell.getEvents'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('intell.getEvents'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", form = form)

@user.route("/logout", methods = ['GET'])
def logout():
    logout_user()
    return redirect(url_for('intell.getEvents'))

@user.route("/isAuthenticated")
def isAuthenticated():
    return jsonify(current_user.is_authenticated)