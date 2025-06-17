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

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':  
    app.run(debug=True)

flask-app/
  static/
    1.jpg
    2.jpg
    3.jpg
    4.jpg
    5.jpg
    6.jpg
    7.jpg
    8.jpg
    9.jpg
    10.jpg
    templates/
        pythonofsf.html
        profile.html
        login.html
        signup.html