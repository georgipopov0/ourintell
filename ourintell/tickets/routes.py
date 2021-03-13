from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user
import json

tickets = Blueprint('tickets',__name__)


@tickets.route('/tickets', methods = ["GET"])
@login_required
def get_tickets():
    user_subscriptions = current_user.subscriptions
    user_tickets =[subscription.sent_tickets for subscription in user_subscriptions]
    # Flatten the list
    user_tickets = [item for sublist in user_tickets
                    for item in sublist]

    
    return render_template('notifications.html', tickets = user_tickets)