from flask import request, Blueprint, jsonify, render_template, url_for

from ourintell import db
from ourintell.user.forms import LoginForm

from sqlalchemy import exc

import json 
from hashlib import sha256

user = Blueprint('user',__name__)

@user.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form = form)