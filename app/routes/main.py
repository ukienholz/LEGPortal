from flask import Blueprint, render_template
from app.models import LEG

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    legs_aktiv = LEG.query.filter(LEG.status.in_(['gegründet', 'aktiv'])).order_by(LEG.created_at.desc()).all()
    legs_in_gründung = LEG.query.filter_by(status='in_gründung').order_by(LEG.created_at.desc()).all()
    return render_template('index.html', legs_aktiv=legs_aktiv, legs_in_gründung=legs_in_gründung)


@bp.route('/info')
def info():
    return render_template('info.html')
