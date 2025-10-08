from numbers import Number

from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
import email_validator

class LoginForm(FlaskForm):
    email = StringField('Email /Phone', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired(),Length(min=3, max=30),  Regexp(r'^[A-Za-z]+(?: [A-Za-z]+)*$', message="Only letters are allowed.")])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Regexp(r'^0\d{10,}$', message="Enter a valid phone number")])
    select_course = SelectField('Select a course', validators=[DataRequired()], choices=[
        ('', '-- Select a course --'),
        ('sales-and-copywriting', 'Sales & Copywriting'),
        ('technical-writing','Technical Writing'),
        ('digital-marketing','Digital Marketing'),
        ('email-marketing','Email Marketing'),
        ('content-writing','Content-Writing'),
        ('scriptwriting', 'ScriptWriting'),
        ('creative-writing', 'Creative Writing'),
        ('virtual-assistance','Virtual Assistant'),
        ('voice-over-acting','Voice Over Acting'),
        ('video-editing&motion-graphics','Video Editing & Motion Graphics'),
        ('smartphone-video-editing','Smartphone Video Editing'),
        ('graphics-design','Graphics Design'),
        ('frontend - development',''),
        ('backend-development','Backend Development'),
        ('project-management','Project Management'),
        ('ui-ux-design','UI/UX Design'),
        ('data-analysis','Data Analysis'),
        ('product-management','Product Management'),
        ('hr-tech-management-system','HR & Tech Management')])

    funnel = SelectField('How did you hear about us?', validators=[DataRequired()], choices=[
        ('', '-- Select --'),
        ('linkedin', 'LinkedIn'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('fnf','Family/friends'),
        ('website','Our Website')])

    gender = SelectField('Gender', validators=[DataRequired()], choices=[
        ('', '-- Select gender --'),
        ('male', 'Male'),
        ('female', 'Female')])

    check_box = BooleanField('Accept Terms & Privacy', default=True)

    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):
    profile_picture =""
    bio = StringField('Bio', validators=[Length(min=3, max=300)])
    interests= SelectField('Learning Interests', validators=[DataRequired()])
    submit = SubmitField('Submit')

class VerifyForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    otp = StringField('OTP', validators=[DataRequired(),Length(min=3, max=8)])
    submit = SubmitField('Submit')

class SlidetextForm(FlaskForm):
    header_text = TextAreaField('Enter text for header slide')
    home_text = TextAreaField ('Enter text for homepage slide')