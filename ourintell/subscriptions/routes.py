from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user

from ourintell import db
from ourintell.models import Subscription, TicketingMethod, TrackableResourceType
from ourintell.subscriptions.forms import CreateSubscriptionForm
from ourintell.subscriptions.utils import send_verification_email


subscriptions = Blueprint('subscriptions', __name__)


@subscriptions.route("/subscriptions", methods = ["GET","POST"])
@login_required
def get_subscriptions():
    user_subscriptions = current_user.subscriptions
    return render_template("subscriptions.html", title='Subscriptions', subscriptions=user_subscriptions)


@subscriptions.route("/create_subscription", methods = ["GET","POST"])
@login_required
def create_subscription():

    # Get all available ticketing methods and resource types
    methods = [method.method  for method in TicketingMethod.query.all()]
    types = [resource.resource_type for resource in TrackableResourceType.query.all()]

    # Generate the form
    form = CreateSubscriptionForm()
    form.ticketing_method.choices = methods
    form.tracked_resource_type.choices = types

    # Create a db entry with the new subscription
    if form.validate_on_submit():
        user = current_user
        subscription = Subscription(userId = current_user.id,
                                     tracked_resource = form.tracked_resource.data, 
                                     tracked_resource_type = form.tracked_resource_type.data, 
                                     ticketing_method = form.ticketing_method.data, 
                                     ticketing_address = form.ticketing_address.data, 
                                     is_verified = False)
        db.session.add(subscription)
        db.session.commit()
        flash('New subscription added','success' )
        send_verification_email(subscription)
        redirect(url_for('subscriptions.get_subscriptions'))
        return redirect(url_for('subscriptions.get_subscriptions'))

    return render_template("create_subscription.html", title='New Subscription', form=form)

@subscriptions.route("/verify_subscription/<token>", methods = ["GET"])
def verify_subscription(token):
    subscription = Subscription.verify_token(token)
    if(token == None):
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('subscriptions.get_subscriptions'))
    subscription.is_verified = True
    db.session.commit()
    flash('The subscription has been verified', 'success')
    return redirect(url_for('subscriptions.get_subscriptions'))

