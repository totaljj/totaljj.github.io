from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional # Allow empty search

class SearchForm(FlaskForm):
    search_term = StringField('Search', validators=[Optional()])
    submit = SubmitField('Search')
