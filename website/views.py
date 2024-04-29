from flask import Blueprint ,render_template,request,flash,jsonify
from flask_login import current_user, login_required
from . import db
from .models import User,Note
import json

views=Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note=request.form.get('note')
        
        if len(note)<1:
            flash('length of note is too short!',category='error')
        else:
            flash('added successfully',category='success')
            
            
        print(note)
        new_note=Note(data=note,user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
    return render_template('home.htm',user=current_user)

@views.route('/pricing')
def price():
    return render_template('pricing.htm')

@views.route('delete-note',methods=['POST'])
def deleteNote():
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})
            