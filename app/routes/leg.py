from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import LEG, Mitgliedschaft
from app.forms import LEGGründenForm, LEGBearbeitenForm

bp = Blueprint('leg', __name__, url_prefix='/leg')


@bp.route('/gründen', methods=['GET', 'POST'])
@login_required
def gründen():
    form = LEGGründenForm()
    if form.validate_on_submit():
        leg = LEG(
            name=form.name.data,
            beschreibung=form.beschreibung.data,
            rechtsform=form.rechtsform.data,
            zweck=form.zweck.data,
            einzugsgebiet=form.einzugsgebiet.data,
            adresse=form.adresse.data,
            plz=form.plz.data,
            ort=form.ort.data,
            kanton=form.kanton.data,
            anteilschein_betrag=form.anteilschein_betrag.data,
            min_anteilscheine=form.min_anteilscheine.data or 1,
            registrierung_offen=form.registrierung_offen.data,
            gründer_id=current_user.id,
        )
        db.session.add(leg)
        db.session.flush()

        # Gründer wird automatisch als aktives Mitglied mit Rolle "gründer" eingetragen
        mitgliedschaft = Mitgliedschaft(
            user_id=current_user.id,
            leg_id=leg.id,
            rolle='gründer',
            status='aktiv',
            bestätigt_am=datetime.now(timezone.utc),
        )
        db.session.add(mitgliedschaft)
        db.session.commit()
        flash(f'LEG "{leg.name}" wurde erfolgreich erstellt!', 'success')
        return redirect(url_for('leg.detail', leg_id=leg.id))
    return render_template('leg/gründen.html', form=form)


@bp.route('/<int:leg_id>')
def detail(leg_id):
    leg = db.session.get(LEG, leg_id)
    if not leg:
        flash('LEG nicht gefunden.', 'danger')
        return redirect(url_for('main.index'))

    ist_mitglied = False
    mitgliedschaft = None
    ist_gründer = False
    if current_user.is_authenticated:
        mitgliedschaft = Mitgliedschaft.query.filter_by(
            user_id=current_user.id, leg_id=leg.id
        ).first()
        ist_mitglied = mitgliedschaft is not None and mitgliedschaft.status == 'aktiv'
        ist_gründer = leg.gründer_id == current_user.id

    rechtsform_label = dict(LEG.RECHTSFORMEN).get(leg.rechtsform, leg.rechtsform)
    status_label = dict(LEG.STATUS_OPTIONEN).get(leg.status, leg.status)

    return render_template('leg/detail.html',
                           leg=leg,
                           ist_mitglied=ist_mitglied,
                           mitgliedschaft=mitgliedschaft,
                           ist_gründer=ist_gründer,
                           rechtsform_label=rechtsform_label,
                           status_label=status_label)


@bp.route('/<int:leg_id>/bearbeiten', methods=['GET', 'POST'])
@login_required
def bearbeiten(leg_id):
    leg = db.session.get(LEG, leg_id)
    if not leg:
        flash('LEG nicht gefunden.', 'danger')
        return redirect(url_for('main.index'))
    if leg.gründer_id != current_user.id:
        flash('Nur der/die Gründer/in kann die LEG bearbeiten.', 'danger')
        return redirect(url_for('leg.detail', leg_id=leg.id))

    form = LEGBearbeitenForm(obj=leg)
    if form.validate_on_submit():
        form.populate_obj(leg)
        db.session.commit()
        flash('LEG wurde aktualisiert.', 'success')
        return redirect(url_for('leg.detail', leg_id=leg.id))
    return render_template('leg/bearbeiten.html', form=form, leg=leg)


@bp.route('/meine')
@login_required
def meine_legs():
    gegründete = LEG.query.filter_by(gründer_id=current_user.id).all()
    mitgliedschaften = Mitgliedschaft.query.filter_by(user_id=current_user.id).all()
    beigetretene_leg_ids = {m.leg_id for m in mitgliedschaften if m.leg_id not in {l.id for l in gegründete}}
    beigetretene = LEG.query.filter(LEG.id.in_(beigetretene_leg_ids)).all() if beigetretene_leg_ids else []
    return render_template('leg/meine_legs.html',
                           gegründete=gegründete,
                           beigetretene=beigetretene,
                           mitgliedschaften={m.leg_id: m for m in mitgliedschaften})
