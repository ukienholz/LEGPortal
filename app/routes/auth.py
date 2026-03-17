from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import LoginForm, RegistrierungForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/registrieren', methods=['GET', 'POST'])
def registrieren():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrierungForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Diese E-Mail-Adresse ist bereits registriert.', 'danger')
            return render_template('auth/registrieren.html', form=form)
        user = User(
            email=form.email.data,
            vorname=form.vorname.data,
            nachname=form.nachname.data,
            telefon=form.telefon.data,
            adresse=form.adresse.data,
            plz=form.plz.data,
            ort=form.ort.data,
            kanton=form.kanton.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registrierung erfolgreich! Sie können sich jetzt anmelden.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/registrieren.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ungültige E-Mail-Adresse oder Passwort.', 'danger')
            return render_template('auth/login.html', form=form)
        login_user(user)
        next_page = request.args.get('next')
        flash(f'Willkommen, {user.vorname}!', 'success')
        return redirect(next_page or url_for('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sie wurden abgemeldet.', 'info')
    return redirect(url_for('main.index'))


@bp.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    form = RegistrierungForm(obj=current_user)
    if request.method == 'GET':
        form.password.data = ''
        form.password2.data = ''
    if form.validate_on_submit():
        current_user.vorname = form.vorname.data
        current_user.nachname = form.nachname.data
        current_user.telefon = form.telefon.data
        current_user.adresse = form.adresse.data
        current_user.plz = form.plz.data
        current_user.ort = form.ort.data
        current_user.kanton = form.kanton.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Profil wurde aktualisiert.', 'success')
        return redirect(url_for('auth.profil'))
    return render_template('auth/profil.html', form=form)
