from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField, IntegerField, DateTimeField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Length


class ExperimentForm(FlaskForm):
    dataset = RadioField('Dataset:', choices=[('original,output sat 1.1,output sat 1.5', 1), ('original,output wp 500,output wp 1000', 2)], validators=[DataRequired()])
    time_to_response = DateTimeField('Time to response:', format='%M:%S')
    amount_of_pic = IntegerField('Amount of dataset pic:') 
    config_name = StringField('Experiment name:')
    submit = SubmitField('Save')

class LoadExperimentForm(FlaskForm):
    config_file = FileField('Select config file:')
    submit = SubmitField('Load')

class IntervieweeForm(FlaskForm):
    name = StringField('Your name:')
    age = IntegerField('Age:')
    gender = RadioField('Gender:', choices=[('male', 'Male'), ('female', 'Female')])
    education = TextAreaField('Your education:')
    submit = SubmitField('Continue')