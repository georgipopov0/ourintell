from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user

from ourintell import db
from ourintell.models import Subscription, TicketingMethod, TrackableResourceType
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

    methods = [method.method  for method in TicketingMethod.query.all()]
    types = [resource.resource_type for resource in TrackableResourceType.query.all()]

    form = CreateSubscriptionForm()
    form.ticketing_method.choices = methods
    form.ticketing_method.default = 'email'
    form.tracked_resource_type.choices = types

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
        redirect(url_for('subscriptions.get_subscriptions'))
        return redirect(url_for('subscriptions.get_subscriptions'))

    return render_template("create_subscription.html", title='New Subscription', form=form)

