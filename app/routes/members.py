from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import LEG, Mitgliedschaft
from app.forms import MitgliedBeitretenForm

bp = Blueprint('members', __name__, url_prefix='/mitglieder')


@bp.route('/beitreten/<int:leg_id>', methods=['GET', 'POST'])
@login_required
def beitreten(leg_id):
    leg = db.session.get(LEG, leg_id)
    if not leg:
        flash('LEG nicht gefunden.', 'danger')
        return redirect(url_for('main.index'))

    if not leg.registrierung_offen:
        flash('Die Mitglieder-Registrierung für diese LEG ist geschlossen.', 'warning')
        return redirect(url_for('leg.detail', leg_id=leg.id))

    bestehend = Mitgliedschaft.query.filter_by(user_id=current_user.id, leg_id=leg.id).first()
    if bestehend:
        if bestehend.status == 'aktiv':
            flash('Sie sind bereits Mitglied dieser LEG.', 'info')
        elif bestehend.status == 'ausstehend':
            flash('Ihr Beitrittsantrag wird noch bearbeitet.', 'info')
        else:
            flash(f'Status Ihrer Mitgliedschaft: {bestehend.status}', 'info')
        return redirect(url_for('leg.detail', leg_id=leg.id))

    form = MitgliedBeitretenForm()
    if leg.min_anteilscheine:
        form.anzahl_anteilscheine.validators[1].min = leg.min_anteilscheine

    if form.validate_on_submit():
        mitgliedschaft = Mitgliedschaft(
            user_id=current_user.id,
            leg_id=leg.id,
            rolle='mitglied',
            status='ausstehend',
            anzahl_anteilscheine=form.anzahl_anteilscheine.data,
        )
        db.session.add(mitgliedschaft)
        db.session.commit()
        flash('Ihr Beitrittsantrag wurde eingereicht. Der/die Gründer/in wird diesen prüfen.', 'success')
        return redirect(url_for('leg.detail', leg_id=leg.id))

    return render_template('members/beitreten.html', form=form, leg=leg)


@bp.route('/verwalten/<int:leg_id>')
@login_required
def verwalten(leg_id):
    leg = db.session.get(LEG, leg_id)
    if not leg:
        flash('LEG nicht gefunden.', 'danger')
        return redirect(url_for('main.index'))
    if leg.gründer_id != current_user.id:
        flash('Nur der/die Gründer/in kann Mitglieder verwalten.', 'danger')
        return redirect(url_for('leg.detail', leg_id=leg.id))

    mitgliedschaften = Mitgliedschaft.query.filter_by(leg_id=leg.id).all()
    mitglieder_details = []
    for m in mitgliedschaften:
        from app.models import User
        user = db.session.get(User, m.user_id)
        mitglieder_details.append({'mitgliedschaft': m, 'user': user})

    return render_template('members/verwalten.html', leg=leg, mitglieder=mitglieder_details)


@bp.route('/bestätigen/<int:mitgliedschaft_id>')
@login_required
def bestätigen(mitgliedschaft_id):
    mitgliedschaft = db.session.get(Mitgliedschaft, mitgliedschaft_id)
    if not mitgliedschaft:
        flash('Mitgliedschaft nicht gefunden.', 'danger')
        return redirect(url_for('main.index'))

    leg = db.session.get(LEG, mitgliedschaft.leg_id)
    if leg.gründer_id != current_user.id:
        flash('Keine Berechtigung.', 'danger')
        return redirect(url_for('main.index'))

    mitgliedschaft.status = 'aktiv'
    mitgliedschaft.bestätigt_am = datetime.now(timezone.utc)
    db.session.commit()

    from app.models import User
    user = db.session.get(User, mitgliedschaft.user_id)
    flash(f'Mitgliedschaft von {user.vorname} {user.nachname} wurde bestätigt.', 'success')
    return redirect(url_for('members.verwalten', leg_id=leg.id))


@bp.route('/ablehnen/<int:mitgliedschaft_id>')
@login_required
def ablehnen(mitgliedschaft_id):
    mitgliedschaft = db.session.get(Mitgliedschaft, mitgliedschaft_id)
    if not mitgliedschaft:
        flash('Mitgliedschaft nicht gefunden.', 'danger')
        return redirect(url_for('main.index'))

    leg = db.session.get(LEG, mitgliedschaft.leg_id)
    if leg.gründer_id != current_user.id:
        flash('Keine Berechtigung.', 'danger')
        return redirect(url_for('main.index'))

    mitgliedschaft.status = 'abgelehnt'
    db.session.commit()

    from app.models import User
    user = db.session.get(User, mitgliedschaft.user_id)
    flash(f'Mitgliedschaft von {user.vorname} {user.nachname} wurde abgelehnt.', 'warning')
    return redirect(url_for('members.verwalten', leg_id=leg.id))
