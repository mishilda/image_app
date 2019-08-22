from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField, IntegerField, DateTimeField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Length


class ExperimentForm(FlaskForm):
    dataset = RadioField('Dataset:', choices=[('original,output sat 1.1,output sat 1.5', 1), ('original,output wp 500,output wp 1000', 2)], validators=[DataRequired()])
    time_to_response = IntegerField('Time to response in sec:', validators=[DataRequired()])
    amount_of_pic = IntegerField('Amount of dataset pic:', validators=[DataRequired()]) 
    config_name = StringField('Experiment name:')
    submit = SubmitField('Save')

class LoadExperimentForm(FlaskForm):
    config_file = FileField('Select config file:', validators=[DataRequired()])
    submit = SubmitField('Load')

class IntervieweeForm(FlaskForm):
    name = StringField('Your name:', validators=[DataRequired()])
    age = IntegerField('Age:', validators=[DataRequired()])
    gender = RadioField('Gender:', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    education = TextAreaField('Your education:')
    submit = SubmitField('Continue')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment:')
    submit = SubmitField('Send')