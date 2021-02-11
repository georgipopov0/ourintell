from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class CreateSubscriptionForm(FlaskForm):
    ticketing_method = SelectField('TicketingMethod',
                           validators=[DataRequired(), Length(min=2, max=20)])
    ticketing_address = StringField('Address',
                           validators=[DataRequired(),])
    tracked_resource_type = SelectField('ResourceType',
                        validators=[DataRequired(),])
    tracked_resource = StringField('TrackResource', validators=[DataRequired()])
    submit = SubmitField('Submit')