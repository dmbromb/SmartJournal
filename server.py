from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
import os
import calendar

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


# CREATE USER DATABASE
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    last_signed_in = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    sign_in_count = db.Column(db.Integer, default=0)
    journal_entry = db.relationship('Journal_Entry', back_populates='user', cascade="all, delete-orphan")


class Journal_Entry(db.Model):
    __tablename__ = 'journal_entry'
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String(10000))
    entry_date = db.Column(db.String(15), default=datetime.now().strftime('%Y-%m-%d'))
    created_on = db.Column(db.DateTime, default=datetime.now())
    last_edited = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='journal_entry')


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('dashboard', name=name))
        else:
            flash("Wrong Code. Contact Admin")
    return render_template("register.html", error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user:
            flash('Invalid credentials')
        elif check_password_hash(user.password, password):
            user.last_signed_in = datetime.now()  # Update last_signed_in
            user.sign_in_count += 1
            db.session.commit()  # Save the change
            login_user(user)
            return redirect(url_for('dashboard', name=user.name))
        else:
            flash('Invalid Password')
    return render_template("login.html", error=error)


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", logged_in=True, today = datetime.now().strftime('%Y-%m-%d'))


@app.route('/new_entry/<date>', methods=['GET', 'POST'])
def new_entry(date):
    if not date:
        today = datetime.now().strftime('%Y-%m-%d')
    else:
        today = date
    if request.method == 'POST':
        journal_entry = request.form.get('journal_entry')
        # Save in database
        new_entry = Journal_Entry(
            entry=journal_entry,
            user_id=current_user.id,
            entry_date=today
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template("new_entry.html", logged_in=True, date=today)


@app.route('/view_past_entries')
@login_required
def view_past_entries():
    month = request.args.get('month', default=datetime.now().month, type=int)
    year = request.args.get('year', default=datetime.now().year, type=int)
    now = datetime(year, month, 1)

    cal = calendar.Calendar()
    month_days = [(day, (datetime(year, month, day).weekday() if day else None)) for day in cal.itermonthdays(year, month)]

    user_entries = db.session.query(Journal_Entry).filter_by(user_id=current_user.id).all()
    entry_dates = [entry.entry_date for entry in user_entries]

    return render_template("view_past_entries.html", logged_in=True, month_days=month_days, now=now, year=year, month=month, entry_dates=entry_dates)

@app.route('/view_entry/<entry_date>')
@login_required
def view_entry(entry_date):
    entry_date_obj = datetime.strptime(entry_date, '%Y-%m-%d').date()
    entry = db.session.query(Journal_Entry).filter(
        db.func.date(Journal_Entry.entry_date) == entry_date_obj,
        Journal_Entry.user_id == current_user.id
    ).first_or_404()
    return render_template('view_entry.html', date=entry_date, entry=entry)


@app.route('/delete_entry', methods=['POST'])
@login_required
def delete_entry():
    date = request.form.get('entry_date')
    entry_date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    entry = db.session.query(Journal_Entry).filter(
        db.func.date(Journal_Entry.entry_date) == entry_date_obj,
        Journal_Entry.user_id == current_user.id
    ).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('view_past_entries'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
