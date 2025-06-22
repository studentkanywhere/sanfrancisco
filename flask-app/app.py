from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)  # <-- Add this line
    hobbies = db.relationship('Hobby', backref='user', lazy=True)

class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hobby = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    users = User.query.all()
    return render_template('pythonofsf.html', users=users)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)
   
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email , password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        hobbies = request.form.getlist('hobbies[]')
        # TODO: Validate and save user
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))
        
        if User.query.filter((User.email == email) | (User.username == username)).first():
            flash('Email or usernamealready exists')
            return redirect(url_for('signup'))
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        for h in hobbies:
            if h.strip():
                db.session.add(Hobby(hobby=h.strip(), user_id=user.id))
        db.session.commit()

        flash('Account created! PLease sign in.')
        return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        hobbies = request.form.getlist('hobbies[]')

        # Check for username/email conflicts (excluding current user)
        if User.query.filter(User.username == username, User.id != user.id).first():
            flash('Username already taken')
            return redirect(url_for('edit_profile'))
        if User.query.filter(User.email == email, User.id != user.id).first():
            flash('Email already taken')
            return redirect(url_for('edit_profile'))

        user.username = username
        user.email = email

        # Update hobbies: remove old, add new
        Hobby.query.filter_by(user_id=user.id).delete()
        for h in hobbies:
            if h.strip():
                db.session.add(Hobby(hobby=h.strip(), user_id=user.id))
        db.session.commit()

        flash('Profile updated!')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('signin'))


if __name__ == '__main__':  
    app.run(host ='0.0.0.0', port = 5000, debug=True)