from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from global_health_tracker import app, db
from global_health_tracker.models import User, Outbreak
from global_health_tracker.forms import RegisterForm, LoginForm, SearchForm
from global_health_tracker.db_queries import get_outbreaks_by_country, get_user_search_history, add_user_search_history
from flask_bcrypt import Bcrypt  # Import Bcrypt

bcrypt = Bcrypt(app)  # Initialize Bcrypt with the Flask app


# Home route
@app.route('/')
def home():
    return render_template('home.html')


# Search route
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()

    if form.validate_on_submit():
        country = form.country.data
        year = form.year.data

        # Record user search history
        add_user_search_history(current_user.id, country)

        # Get disease outbreaks based on user's search
        outbreaks = get_outbreaks_by_country(country, years=10)

        return render_template('results.html', outbreaks=outbreaks)

    return render_template('search.html', form=form)


# History route
@app.route('/history')
@login_required
def history():
    # Get user search history
    search_history = get_user_search_history(current_user.id)
    return render_template('history.html', search_history=search_history)


# Other routes (login, logout, register)...

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # Use bcrypt here
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', form=form)


# logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Use bcrypt here
        new_user = User(email=form.email.data, password=hashed_password, first_name=form.first_name.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html', form=form)
