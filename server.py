from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['TEMPLATES_AUTO_RELOAD'] = True
login_manager = LoginManager()
login_manager.init_app(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main_database.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#CREATE USER DATABASE
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    last_signed_in = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    sign_in_count = db.Column(db.Integer, default=0)


with app.app_context():
    db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/register', methods = ['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if db.session.execute(db.select(User).where(User.email == email)).scalar():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        # access_code = request.form.get('access code')
        # if access_code == ACCESS_CODE:
        if True:
            hashed_password = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)
            new_user = User(
                name=name,
                email=email,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard', name = name))
        else:
            flash("Wrong Code. Contact Admin")
    return render_template("register.html", error = error)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user:
            flash('Invalid credentials')
        elif check_password_hash(user.password,password):
            user.last_signed_in = datetime.now()  # Update last_signed_in
            user.sign_in_count += 1
            db.session.commit()  # Save the change
            login_user(user)
            return redirect(url_for('dashboard', name = user.name))
        else:
            flash('Invalid Password')
    return render_template("login.html", error = error)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", logged_in=True)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
