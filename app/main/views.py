from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from app import db, bcrypt, create_app
from app.models import User, Pitch, Booking
from .forms import RegistrationForm, LoginForm, ContactForm, BookingForm, Booking, PitchoccupationForm, PitchavailableForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home'

    return render_template('index.html', title = title )
@main.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/contact-us", methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    return render_template('contact.html', title='Contact Us', form=form)



@main.route('/bookingbooker')
def booking():
    bookings=Booking.query.order_by(Booking.date).all()
    bookingreturns=[]
    for booking in bookings:
        bookingreturn=dict()
        bookingreturn['title']=booking.title
        # bookingreturn['team']=Team.query.filter_by(id=booking.teamId).first().teamName
        bookingreturn['pitch']=Pitch.query.filter_by(id=booking.pitchId).first().pitchName
        bookingreturn['booker']=User.query.filter_by(id=booking.bookerId).first().fullname
        bookingreturn['date']=booking.date.date()
        bookingreturn['time']=f'{booking.startTime} to {booking.endTime}'
        bookingreturns.append(bookingreturn)
    return render_template('booking.html',bookings=bookingreturns)

@main.route('/book',methods=['GET','POST'])
@login_required
def book():
    form=BookingForm()
    if form.validate_on_submit():
        
        # check time collision
        bookingcollisions=Booking.query.filter_by(date=datetime.combine(form.date.data,datetime.min.time())).filter_by(pitchId=form.pitchs.data).all()
        print(len(bookingcollisions))
        for bookingcollision in bookingcollisions:
            if (form.startTime.data<bookingcollision.endTime and (form.startTime.data+form.duration.data)>bookingcollision.startTime):
                flash(f'The time from {bookingcollision.startTime} to {bookingcollision.endTime} is already booked by {User.query.filter_by(id=bookingcollision.bookerId).first().fullname}.')
                return redirect(url_for('main.book'))

        # make booking
        booker=current_user
        pitch=Pitch.query.filter_by(id=form.pitchs.data).first()
        endTime=form.startTime.data+form.duration.data
        booking=Booking(pitchId=pitch.id,bookerId=booker.id,date=form.date.data,startTime=form.startTime.data,endTime=endTime,duration=form.duration.data)
        db.session.add(booking)
        db.session.commit()
        flash('Booking success!')
        return redirect(url_for('main.index'))
    return render_template('book.html',title='Book Booking',form=form)


@main.route('/pitchavailable',methods=['GET','POST'])
def pitchavailable():
    form=PitchavailableForm()
    if form.validate_on_submit():
        bookings=Booking.query.filter_by(date=datetime.combine(form.date.data,datetime.min.time())).all()
        pitchsOccupied=set()
        for booking in bookings:
            if (form.startTime.data<booking.endTime and (form.startTime.data+form.duration.data)>booking.startTime): 
                pitchsOccupied.add(Pitch.query.filter_by(id=booking.pitchId).first())
        pitchs=Pitch.query.all()
        pitchsavailable=[]
        for pitch in pitchs:
            if pitch not in pitchsOccupied:
                pitchsavailable.append(pitch)
        return render_template('pitchavailablelist.html',title='Pitch available',pitchs=pitchsavailable)
    return render_template('pitchavailable.html',title='Pitch availability check',form=form)

@main.route('/pitchoccupation',methods=['GET','POST'])
def pitchoccupation():
    form=PitchoccupationForm()
    if form.validate_on_submit():
        #bookings=Booking.query.filter_by(date=datetime.combine(form.date.data,datetime.min.time())).all()
        pitchoccus=[]
        hours=range(9,23)
        pitchs=Pitch.query.all()
        allpitchs=[]
        for pitch in pitchs:
            pitchoccu=dict()
            pitchoccu['pitchName']=pitch.pitchName
            pitchoccu['pitchhours']=[False]*14
            for hour in hours:
                bookings=Booking.query.filter_by(date=datetime.combine(form.date.data,datetime.min.time())).filter_by(pitchId=pitch.id).all()
                
                for booking in bookings:
                    if (hour+0.5)<booking.endTime and (hour+0.5)>booking.startTime:
                        pitchoccu['pitchhours'][hour-9]=True
                        break
            pitchoccus.append(pitchoccu)
            
            allpitchs.append({'pitchName':pitch.pitchName,'tel':'Yes' if pitch.telephone else 'No','pro':'Yes' if pitch.projector else 'No',\
                             'wb':'Yes' if pitch.whiteboard else 'No','cost':pitch.cost})
        return render_template('pitchoccupationlist.html',title='Pitch Occupation',pitchoccus=pitchoccus,date=form.date.data,hours=[str(hour) for hour in hours],allpitchs=allpitchs)
    return render_template('pitchoccupation.html',title='Pitch Occupation Status',form=form)
