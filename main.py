from flask import Flask, render_template, request, url_for, redirect, session, g
import re, os
from datetime import timedelta


app = Flask(__name__)


    
  

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=1)
subscribers = []


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title = 'home')



@app.route('/about')
def about():
    return render_template("about.html", title = 'About')



@app.route('/contact')
def contact():
    return render_template("contact.html",  title = 'Contact')



@app.route('/register')
def register():
    return render_template("register.html",  title = 'register')



@app.route('/database', methods=["POST"])
def datab():
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    name = request.form.get("nm")
    email = request.form.get("email")
    password = request.form.get("password")
    repeat_password = request.form.get("repeat_password")
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if mat:
        #პაროლი უნდა იყოს მსგავსი ფორმატის Geek12@
        subscribers.append(f"{name} {email} {password}")
        return render_template("database.html",  title = 'database', name = name, email= email, password= password, repeat_password = repeat_password, subscribers = subscribers)
    else:
        return f"Password doesn't meet complexity requirements !!"
    
    
    
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session.permanent = True
        session.pop('user', None) 
        if request.form['password'] == 'Geek12@':
            session['user'] = request.form['email']
            return redirect(url_for('protected'))
            
    return render_template("login.html",  title = 'login')



@app.route('/protected', methods=["GET", "POST"])
def protected():
    if g.user:
        return render_template("protected.html", user = session['user'],  title = 'protected')
    return redirect(url_for('login'))
   
       
            
@app.before_request
def before_request():
    g.user = None
    
    if 'user' in session:
        g.user = session['user']
        
          
          
@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return render_template('home.html')
       









if __name__ == '__main__':
    app.run(debug=True)