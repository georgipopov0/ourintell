from flask import Blueprint, render_template, url_for
from flask_login import login_required

from ourintell.models import Subscription, TicketingMethod, TrackableResource
from ourintell.subscriptions.forms import CreateSubscriptionForm

subscriptions = Blueprint('subscriptions', __name__)

@subscriptions.route("/subscriptions", methods = ["GET"])
@login_required
def get_subscriptions():
    subscriptions = Subscription.query.all()
    methods = [method.ticketingMethod  for method in TicketingMethod.query.all()]
    trackable_resources = TrackableResource.query.all()
    types = [resource.resourceName for resource in trackable_resources]

    form = CreateSubscriptionForm()
    form.ticketingMethod.choices = methods
    form.trackedResourceType.choices = types

    return render_template("subscriptions.html", title='Subscriptions', subscriptions=subscriptions, form=form)