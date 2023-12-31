# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Search')