from flask import request, Blueprint, jsonify, render_template, url_for

from ourintell import db
from sqlalchemy import exc

import json 
from hashlib import sha256

user = Blueprint('user',__name__)

@user.route("/hi")
def hi():
    return "hi"