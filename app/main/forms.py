from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# from flaskblog.models import User


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



# class BookmeetingForm(FlaskForm):
#     title=StringField('Meeting title',validators=[DataRequired()])
#     rooms=SelectField('Choose room',coerce=int,choices=RoomChoiceIterable())
#     date=DateField('Choose date', format="%m/%d/%Y",validators=[DataRequired()])
#     startTime=SelectField('Choose starting time(in 24hr expression)',coerce=int,choices=[(i,i) for i in range(9,19)])
#     duration=SelectField('Choose duration of the meeting(in hours)',coerce=int,choices=[(i,i) for i in range(1,6)])
#     participants_user=SelectMultipleField('Choose participants from company',coerce=int,choices=UserChoiceIterable(),option_widget=widgets.CheckboxInput(),widget=widgets.ListWidget(prefix_label=False),validators=[DataRequired()])
#     participants_partner=SelectMultipleField('Choose participants from partners',coerce=int,choices=PartnerChoiceIterable(),option_widget=widgets.CheckboxInput(),widget=widgets.ListWidget(prefix_label=False))
#     submit=SubmitField('Book')

#     def validate_title(self,title):
#         meeting=Meeting.query.filter_by(title=self.title.data).first()
#         if meeting is not None: # username exist
#             raise ValidationError('Please use another meeting title.')

#     def validate_date(self,date):
#         if self.date.data<datetime.datetime.now().date():
#             raise ValidationError('You can only book for day after today.')

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
