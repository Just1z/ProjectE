from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Title', validators=[DataRequired()])
    work_size = StringField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField("Is finished")
    submit = SubmitField('Submit')