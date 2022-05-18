from unicodedata import category
from flask import Blueprint,render_template, request,redirect, url_for, flash
from .models import User
from . import db
from flask_login import login_required,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ["POST","GET"])
def login():
    """this function is used to log the user in"""
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password') 
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in!', category="success")
                login_user(user,remember=True)
                
                return redirect(url_for('views.home',user=current_user))
            #user=current_user is used to pass information to the front end regarding the users being logged in or not
            else:
                flash('Incorrect password',category='error')
        else:
            flash('Email does not exist', category="error")
               
    return render_template('login.html',user=current_user)

@auth.route('/signup',methods = ["POST","GET"])
def signup():
    """this function contains the logic that is used to sign up users"""
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get("password2")
        
        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()
        
        if email_exist:
            flash('email already in use', category="error")
        elif username_exist:
            flash('username already in use, please choose another username', category="error")
        elif len(username)<2:
            flash('username is too short', category="error")
        elif len(password1)<4:
            flash('password is too short', category="error")
        elif password1 !=  password2:
            flash('both password differ', category="error")
        else:
            print('i got here')
            new_user = User(email=email,username=username,password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('user created!', category= 'success')
            print('success')
            
            return redirect(url_for('views.home', user=current_user)) 
            #user=current_user is used to pass information to the front end regarding the users being logged in or not       
            
    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required #this line of code makes sure that this page cannot be reached if the user is not logged in
def logout():
    "this function is used to log the user out"
    logout_user()
    return redirect(url_for('auth.login'))