from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password. Please try again.')
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
            flash('Email or Username already EXISTS')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
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

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        # Only this check is needed:
        if not check_password_hash(user.password, current_password):
            flash('Current password is incorrect')
            return redirect(url_for('change_password'))
        if not new_password.strip():
            flash('New password cannot be empty')
            return redirect(url_for('change_password'))
        if new_password != confirm_new_password:
            flash('New passwords do not match')
            return redirect(url_for('change_password'))

        # Update password
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password has been changed successfully!')
        return redirect(url_for('profile'))

    return render_template('change_password.html')

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        delete_clause = request.form.get('delete_clause')
        required_clause = "I understand that my account will be deleted permanently and cannot be retrieved."
        if username != user.username:
            flash('Username does not match.')
            return redirect(url_for('delete_account'))
        if not check_password_hash(user.password, password):
            flash('Password is incorrect.')
            return redirect(url_for('delete_account'))
        if delete_clause != required_clause:
            flash('You must type the confirmation phrase exactly to delete your account.')
            return redirect(url_for('delete_account'))
        Hobby.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id', None)
        flash('Your account has been deleted.')
        return redirect(url_for('signup'))
    return render_template('delete_account.html', user=user)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user = User.query.get(session['user_id'])
    if user.username != 'admin':
        flash('Access denied.')
        return redirect(url_for('profile'))
    users = User.query.all()
    hobbies = {user.id: [h.hobby for h in user.hobbies] for user in users}
    return render_template('admin.html', users=users, hobbies=hobbies)

@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user = User.query.get(session['user_id'])
    if user.username != 'admin':
        flash('Access denied.')
        return redirect(url_for('profile'))
    user = User.query.get_or_404(user_id)
    user.username = request.form['username']
    user.email = request.form['email']
   
    new_password = request.form['password']
    if not new_password.startswith('pbkdf2:sha256:'):
        user.password = generate_password_hash(new_password)
    else:
        user.password = new_password
    
    new_hobbies = [h.strip() for h in request.form['hobbies'].split(',') if h.strip()]
  
    Hobby.query.filter_by(user_id=user.id).delete()
    
    for hobby in new_hobbies:
        db.session.add(Hobby(hobby=hobby, user_id=user.id))
    db.session.commit()
    flash('User updated successfully.')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('signin'))

if __name__ == '__main__':  
    app.run(host ='0.0.0.0', port = 5000, debug=True)