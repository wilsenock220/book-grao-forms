from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Pitch, Booking
from datetime import datetime


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
                    raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')




class ContactForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('')



# class UserChoiceIterable(object):
#     def __iter__(self):
#         users=User.query.all()
#         choices=[(user.id,f'{user.fullname}, team {Team.query.filter_by(id=user.teamId).first().teamName}') for user in users] 
#         choices=[choice for choice in choices if 'admin' not in choice[1]] # do not delete admin
#         for choice in choices:
#             yield choice

# class DeleteuserForm(FlaskForm):
#     ids=SelectField('Choose User',coerce=int,choices=UserChoiceIterable())
#     submit=SubmitField('Delete')
class PitchChoiceIterable(object):
    def __iter__(self):
        pitchs=Pitch.query.all()
        choices=[(pitch.id,pitch.pitchName) for pitch in pitchs] 
        for choice in choices:
            yield choice  


class BookingForm(FlaskForm):
    pitchs=SelectField('Choose pitch',coerce=int,choices=PitchChoiceIterable())
    date=DateField('Choose date', format="%m/%d/%Y",validators=[DataRequired()])
    startTime=SelectField('Choose starting time(in 24hr expression)',coerce=int,choices=[(i,i) for i in range(9,19)])
    duration=SelectField('Choose duration of the booking(in hours)',coerce=int,choices=[(i,i) for i in range(1,6)])
    submit=SubmitField('Book')
    
    
    
    def validate_title(self,title):
        booking=Booking.query.filter_by(title=self.title.data).first()
        if booking is not None: # username exist
            raise ValidationError('Please use another booking title.')
 
    def validate_date(self,date):
        if self.date.data<datetime.now().date():
            raise ValidationError('You can only book for day after today.')
    
class BookingChoiceIterable(object):
    def __iter__(self):
        bookings=Booking.query.filter_by(bookerId=current_user.id).all()
        choices=[(booking.id,f'{booking.title} in {Pitch.query.filter_by(id=booking.pitchId).first().pitchName} start at {booking.date.date()} from {booking.startTime}') for booking in bookings] 
        for choice in choices:
            yield choice

class CancelbookingForm(FlaskForm):
    #def __init__(self,userId,**kw):
     #   super(CancelbookingForm, self).__init__(**kw)
      #  self.name.userId =userId
    ids=SelectField('Choose booking to cancel',coerce=int,choices=BookingChoiceIterable()) 
    submit=SubmitField('Cancel') 

class PitchavailableForm(FlaskForm):
    date=DateField('Choose date', format="%m/%d/%Y",validators=[DataRequired()])
    startTime=SelectField('Choose starting time(in 24hr expression)',coerce=int,choices=[(i,i) for i in range(9,19)])
    duration=SelectField('Choose duration of the booking(in hours)',coerce=int,choices=[(i,i) for i in range(1,6)])
    submit=SubmitField('Check')


class PitchoccupationForm(FlaskForm):
    date=DateField('Choose date', format="%m/%d/%Y",validators=[DataRequired()])
    submit=SubmitField('Check')




class BookingChoiceAllIterable(object):
    def __iter__(self):
        bookings=Booking.query.all()
        choices=[(booking.id,f'{booking.title} in {Pitch.query.filter_by(id=booking.pitchId).first().pitchName} start at {booking.date.date()} from {booking.startTime}') for booking in bookings] 
        for choice in choices:
            yield choice

# class UpdateAccountForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     picture = FileField('Update Profile Picture', validators=[
#                         FileAllowed(['jpg', 'png'])])
#     submit = SubmitField('Update')

    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.query.filter_by(username=username.data).first()
    #         if user:
    #             raise ValidationError(
    #                 'That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError(
    #                 'That email is taken. Please choose a different one.')


# class RequestResetForm(FlaskForm):
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     submit = SubmitField('Request Password Reset')

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is None:
#             raise ValidationError(
#                 'There is no account with that email. You must register first.')


# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Reset Password')
