# app/app.py

from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.exceptions import HTTPException

from .forms import LoginForm, RegistrationForm, RouteEntryForm
from .models import Inspection, Route, User, db
from .utils import calculate_total_hours, calculate_total_mileage

# Define the blueprint
main = Blueprint('main', __name__)

# Error Handlers
@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return render_template('error.html', error=e), 500

# Routes
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        routes = Route.query.order_by(Route.date.desc()).all()
        return render_template('dashboard.html', routes=routes)
    else:
        routes = Route.query.filter_by(driver_id=current_user.id).order_by(Route.date.desc()).all()
        return render_template('driver_dashboard.html', routes=routes)

@main.route('/route_entry', methods=['GET', 'POST'])
@login_required
def route_entry():
    if current_user.role != 'driver':
        abort(403)
    form = RouteEntryForm()
    if form.validate_on_submit():
        total_mileage = calculate_total_mileage(form.start_mileage.data, form.end_mileage.data)
        total_hours = calculate_total_hours(form.start_time.data, form.finish_time.data)

        standby_in = form.standby_time_in.data
        standby_out = form.standby_time_out.data
        if standby_in and standby_out and standby_out <= standby_in:
            flash('Standby time out must be after standby time in.', 'danger')
            return render_template('route_entry.html', form=form)

        route = Route(
            driver_id=current_user.id,
            date=form.date.data,
            start_time=form.start_time.data,
            finish_time=form.finish_time.data,
            start_mileage=form.start_mileage.data,
            end_mileage=form.end_mileage.data,
            total_mileage=total_mileage,
            container_number=form.container_number.data.upper(),
            chassis_number=form.chassis_number.data.upper(),
            route_from=form.route_from.data.title(),
            route_to=form.route_to.data.title(),
            load_status=form.load_status.data,
            standby_time_in=standby_in,
            standby_time_out=standby_out,
            total_hours=total_hours
        )
        db.session.add(route)
        db.session.commit()

        inspection = Inspection(
            route_id=route.id,
            lights=form.lights.data,
            tires=form.tires.data,
            brakes=form.brakes.data,
            remarks=form.remarks.data
        )
        db.session.add(inspection)
        db.session.commit()

        flash('Route entry submitted successfully.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('route_entry.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
