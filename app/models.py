from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    vorname = db.Column(db.String(80), nullable=False)
    nachname = db.Column(db.String(80), nullable=False)
    telefon = db.Column(db.String(30))
    adresse = db.Column(db.String(200))
    plz = db.Column(db.String(10))
    ort = db.Column(db.String(100))
    kanton = db.Column(db.String(2))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Beziehungen
    gegründete_legs = db.relationship('LEG', backref='gründer', lazy='dynamic',
                                      foreign_keys='LEG.gründer_id')
    mitgliedschaften = db.relationship('Mitgliedschaft', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class LEG(db.Model):
    __tablename__ = 'legs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    beschreibung = db.Column(db.Text)
    rechtsform = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(30), default='in_gründung')
    # Adresse der LEG
    adresse = db.Column(db.String(200))
    plz = db.Column(db.String(10))
    ort = db.Column(db.String(100))
    kanton = db.Column(db.String(2))
    # Gründungsdaten
    gründungsdatum = db.Column(db.Date)
    zweck = db.Column(db.Text)
    einzugsgebiet = db.Column(db.String(300))
    # Genossenschafts-spezifisch
    anteilschein_betrag = db.Column(db.Float)
    min_anteilscheine = db.Column(db.Integer, default=1)
    # Registrierungslink
    registrierung_offen = db.Column(db.Boolean, default=True)
    # Metadaten
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    gründer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Beziehungen
    mitgliedschaften = db.relationship('Mitgliedschaft', backref='leg', lazy='dynamic',
                                       cascade='all, delete-orphan')

    # Mögliche Rechtsformen
    RECHTSFORMEN = [
        ('genossenschaft', 'Genossenschaft'),
        ('verein', 'Verein'),
        ('einfache_gesellschaft', 'Einfache Gesellschaft'),
        ('ag', 'Aktiengesellschaft (AG)'),
        ('gmbh', 'GmbH'),
    ]

    # Status-Optionen
    STATUS_OPTIONEN = [
        ('in_gründung', 'In Gründung'),
        ('gegründet', 'Gegründet'),
        ('aktiv', 'Aktiv'),
        ('aufgelöst', 'Aufgelöst'),
    ]

    KANTONE = [
        ('AG', 'Aargau'), ('AI', 'Appenzell Innerrhoden'), ('AR', 'Appenzell Ausserrhoden'),
        ('BE', 'Bern'), ('BL', 'Basel-Landschaft'), ('BS', 'Basel-Stadt'),
        ('FR', 'Freiburg'), ('GE', 'Genf'), ('GL', 'Glarus'), ('GR', 'Graubünden'),
        ('JU', 'Jura'), ('LU', 'Luzern'), ('NE', 'Neuenburg'), ('NW', 'Nidwalden'),
        ('OW', 'Obwalden'), ('SG', 'St. Gallen'), ('SH', 'Schaffhausen'),
        ('SO', 'Solothurn'), ('SZ', 'Schwyz'), ('TG', 'Thurgau'), ('TI', 'Tessin'),
        ('UR', 'Uri'), ('VD', 'Waadt'), ('VS', 'Wallis'), ('ZG', 'Zug'),
        ('ZH', 'Zürich'),
    ]

    def anzahl_mitglieder(self):
        return self.mitgliedschaften.filter_by(status='aktiv').count()

    def __repr__(self):
        return f'<LEG {self.name}>'


class Mitgliedschaft(db.Model):
    __tablename__ = 'mitgliedschaften'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leg_id = db.Column(db.Integer, db.ForeignKey('legs.id'), nullable=False)
    rolle = db.Column(db.String(30), default='mitglied')
    status = db.Column(db.String(30), default='ausstehend')
    anzahl_anteilscheine = db.Column(db.Integer, default=1)
    beitrittsdatum = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    bestätigt_am = db.Column(db.DateTime)

    # Rollen
    ROLLEN = [
        ('gründer', 'Gründer/in'),
        ('vorstand', 'Vorstand'),
        ('mitglied', 'Mitglied'),
    ]

    # Status-Optionen
    STATUS_OPTIONEN = [
        ('ausstehend', 'Ausstehend'),
        ('aktiv', 'Aktiv'),
        ('abgelehnt', 'Abgelehnt'),
        ('ausgetreten', 'Ausgetreten'),
    ]

    __table_args__ = (
        db.UniqueConstraint('user_id', 'leg_id', name='unique_mitgliedschaft'),
    )

    def __repr__(self):
        return f'<Mitgliedschaft User={self.user_id} LEG={self.leg_id}>'
