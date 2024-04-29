from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in succesfully',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('wrogn password!,Try again...',category='error')
        else:
            flash('User doesn\'t exists,',category='error')
    return render_template('login.htm',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        
        if user:
            flash('email already exists',category='error')

        elif len(email)<4:
            flash('Email must be greater than 3 character',category='error')
            pass
        elif len(firstName)<2:
            flash('Name must be greater than 1 character',category='error')            
            pass
        elif password1!=password2:
            flash('password don\'t match',category='error')
            pass
        elif len(password1)<7:
            flash('length of password atleast 7 chracters',category='error')
            pass
        else:
            new_user=User(email=email,firstName=firstName,password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True )
            flash('account created',category='success')
            return redirect(url_for('views.home'))
            #add user to database



    return render_template('sign_up.htm',user=current_user)
