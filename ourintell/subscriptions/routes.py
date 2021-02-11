from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user

from ourintell import db
from ourintell.models import Subscription, TicketingMethod, TrackableResource
from ourintell.subscriptions.forms import CreateSubscriptionForm


subscriptions = Blueprint('subscriptions', __name__)

@subscriptions.route("/subscriptions", methods = ["GET","POST"])
@login_required
def get_subscriptions():
    subscriptions = Subscription.query.all()
    return render_template("subscriptions.html", title='Subscriptions', subscriptions=subscriptions)



@subscriptions.route("/create_subscription", methods = ["GET","POST"])
@login_required
def create_subscription():

    methods = [method.ticketingMethod  for method in TicketingMethod.query.all()]
    types = [resource.resourceName for resource in TrackableResource.query.all()]

    form = CreateSubscriptionForm()
    form.ticketingMethod.choices = methods
    form.trackedResourceType.choices = types

    if form.validate_on_submit():
        user = current_user
        subscription = Subscription(userId = current_user.id, trackedResource = form.trackedResource.data, trackedResourceType = form.trackedResourceType.data, ticketingMethod = form.ticketingMethod.data, ticketingAddress = form.ticketingAddress.data)
        db.session.add(subscription)
        db.session.commit()
        flash('New subscription added','success' )
        redirect(url_for('subscriptions.get_subscriptions'))
        return redirect(url_for('subscriptions.get_subscriptions'))

    return render_template("create_subscription.html", title='New Subscription', form=form)

