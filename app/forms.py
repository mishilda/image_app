from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, HiddenField, RadioField, TextAreaField, IntegerField,\
                    SubmitField, SelectField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length
from app import app
import pandas as pd

class ExperimentForm(FlaskForm):
    #dataset = HiddenField('Dataset')
    left_dir = StringField('Left pic directory:', validators=[DataRequired()])
    center_dir = StringField('Center pic directory:', validators=[DataRequired()])
    right_dir = StringField('Right pic directory:', validators=[DataRequired()])
   #dataset = StringField('Dataset CSV full path:', validators=[DataRequired()])
    width = StringField('Pic width, px:')
    # left_w = StringField('left window width, px:')
    # right_w = StringField('right window width, px:')
    time_to_response = IntegerField('Time to response in sec:', validators=[DataRequired()], default=30)
    repetitions = IntegerField('Repetitions', default=1, validators=[DataRequired()])
    config_name = StringField('Experiment name:', validators=[DataRequired()])
    task = StringField('Task:', validators=[DataRequired()],
                       default="Выберите изображение, которое вам больше НРАВИТСЯ")
    submit = SubmitField('Save')

    def validate_dataset(self, dataset):
        columns = ['orig', 'left', 'right']
        data = pd.read_csv(dataset.data, sep=",")
        for col in columns:
            if col not in data.columns:
                raise ValidationError('Not all columns')
        for col in data.columns:
            if data[data[col].isnull()].shape[0]:
                raise ValidationError('Empty values')

class LoadExperimentForm(FlaskForm):
    config_file = FileField('Select config file:', validators=[DataRequired()])
    submit = SubmitField('Load')

class IntervieweeForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    age = SelectField('[TODO] Age:', choices=[('<20', '<20'), ('20-25', '20-25'), ('25-35', '25-35'), ('>35', '>35')])
    gender = SelectField('Gender:', choices=[('male', 'Male'), ('female', 'Female')])
    education = SelectField('[TODO] Education:', choices=[('<BSc', '<BSc'), ('BSc-MSc', 'BSc-MSc'), ('PhD+', 'PhD+')])
    vision_health = TextAreaField('Vision health problems (or \'no\'):', validators=[DataRequired()])
    reverse = BooleanField('Reverse:')
    dev = BooleanField('Участвую в разработке тестируемого алгоритма')
    with_comments = BooleanField('With comments:')
    submit = SubmitField('Continue')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment:')
    submit = SubmitField('Send')
