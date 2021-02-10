from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class CreateSubscriptionForm(FlaskForm):
    ticketingMethod = SelectField('TicketingMethod',
                           validators=[DataRequired(), Length(min=2, max=20)])
    ticketingAddress = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])
    trackedResourceType = SelectField('ResourceType',
                        validators=[DataRequired(),])
    trackedResource = StringField('TrackResource', validators=[DataRequired()])
    submit = SubmitField('Submit')