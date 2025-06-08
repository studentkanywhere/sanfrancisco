from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('pythonofsf.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':  
    app.run(debug=True)