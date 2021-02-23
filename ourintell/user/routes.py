from flask import request, Blueprint, jsonify, render_template, url_for, flash, redirect, current_app
from flask_login import current_user, login_user, logout_user


from ourintell import db,  bcrypt
from ourintell.user.forms import LoginForm, RegistrationForm , RequestResetForm, ResetPasswordForm
from ourintell.models import User
from ourintell.user.utils import send_reset_email, send_accaunt_verification_email


from sqlalchemy import exc

import json 
from hashlib import sha256

user = Blueprint('user',__name__)

@user.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('intell.get_events'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_verified = False)
        db.session.add(user)
        db.session.commit()

        send_accaunt_verification_email(user)
        flash(f'A verification email has been sent to {form.email.data}', 'success')
        return redirect(url_for('user.login'))
    return render_template("register.html", form = form)

@user.route("/verify_account/<token>", methods = ["GET"])
def verify_account(token):
    user = User.verify_token(token)
    if(token == None):
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('intell.get_events'))
    user.is_verified = True
    db.session.commit()
    flash('Your account has been verified', 'success')
    return redirect(url_for('intell.get_events'))

@user.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('intell.get_events'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('intell.get_events'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", form = form)


@user.route("/logout", methods = ['GET'])
def logout():
    logout_user()
    return redirect(url_for('intell.get_events'))


@user.route("/reset_password", methods = ["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('intell.get_events'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to change your password', 'success')
        return redirect(url_for('user.login'))
    return render_template('request_reset.html', title='Reset Password', form=form)

@user.route("/reset_password/<token>", methods = ["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('intell.get_events'))
    user = User.verify_token(token)
    if(not user):
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()\

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('user.login'))

    return render_template('reset_password.html', title='Reset Password', form=form)

