from flask_wtf import FlaskForm
from wtforms import (StringField, DateField)
from wtforms.validators import InputRequired, Length, Regexp


class CourseForm(FlaskForm):
    ticker = StringField('Ticker', validators=[InputRequired(),
                                               Length(min=1, max=5), Regexp('[A-Z]+$', message="Ticker must consist of capital letters only")])
    date = DateField('Date', validators=[InputRequired()])
