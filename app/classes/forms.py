# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired
from wtforms.fields.html5 import URLField, DateField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')

class SleepForm(FlaskForm):
    rating = SelectField("Rating", choices=[('---','---'),(1,1),(2,2),(3,3),(4,4),(5,5)])
    hours = IntegerField("Hours")
    sleep_date = DateField("Date")
    submit = SubmitField("Submit")

class BlogForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Blog', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Blog')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')
