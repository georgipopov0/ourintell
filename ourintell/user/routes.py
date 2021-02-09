from flask import request, Blueprint, jsonify, render_template, url_for, flash, redirect

from ourintell import db,  bcrypt
from ourintell.user.forms import LoginForm, RegistrationForm
from ourintell.models import User


from sqlalchemy import exc

import json 
from hashlib import sha256

user = Blueprint('user',__name__)

@user.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
                flash('You have been logged in!', 'success')
                return redirect(url_for("intell.getEvents"))
            else:
              flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", form = form)

@user.route("/register", methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('intell.getEvents'))
    return render_template("register.html", form = form)

@user.route("/addSpas")
def addSpas():
    spas = User(username='Spas', email='spas@spas.spas', password='spas')
    db.session.add(spas)
    db.session.commit()
    return "Spass"