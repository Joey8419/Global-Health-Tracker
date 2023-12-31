# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User
from .forms import RegisterForm, LoginForm, SearchForm
from .db_queries import get_outbreaks_by_country, get_user_search_history, add_user_search_history
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)


# Sample login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('views.home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', form=form)


# Sample logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('views.home'))


# Sample register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(email=form.email.data, password=hashed_password, first_name=form.first_name.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        login_user(new_user)
        return redirect(url_for('views.home'))

    return render_template('register.html', form=form)

# Add more routes for other authentication-related functionalities if needed
