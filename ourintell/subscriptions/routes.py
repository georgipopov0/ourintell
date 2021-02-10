from flask import Blueprint, render_template, url_for

from ourintell.models import Subscription

subscriptions = Blueprint('subscriptions', __name__)

@subscriptions.route("/subscriptions", methods = ["GET"])
def get_subscriptions():
    subscriptions = Subscription.query.all()
    return render_template("subscriptions.html", title='Subscriptions', subscriptions=subscriptions)