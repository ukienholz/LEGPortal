from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, SelectField,
                     FloatField, IntegerField, BooleanField, DateField, SubmitField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Anmelden')


class RegistrierungForm(FlaskForm):
    vorname = StringField('Vorname', validators=[DataRequired(), Length(max=80)])
    nachname = StringField('Nachname', validators=[DataRequired(), Length(max=80)])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    telefon = StringField('Telefon', validators=[Optional(), Length(max=30)])
    adresse = StringField('Adresse', validators=[Optional(), Length(max=200)])
    plz = StringField('PLZ', validators=[Optional(), Length(max=10)])
    ort = StringField('Ort', validators=[Optional(), Length(max=100)])
    kanton = SelectField('Kanton', choices=[('', '-- Bitte wählen --')] + [
        ('AG', 'Aargau'), ('AI', 'Appenzell Innerrhoden'), ('AR', 'Appenzell Ausserrhoden'),
        ('BE', 'Bern'), ('BL', 'Basel-Landschaft'), ('BS', 'Basel-Stadt'),
        ('FR', 'Freiburg'), ('GE', 'Genf'), ('GL', 'Glarus'), ('GR', 'Graubünden'),
        ('JU', 'Jura'), ('LU', 'Luzern'), ('NE', 'Neuenburg'), ('NW', 'Nidwalden'),
        ('OW', 'Obwalden'), ('SG', 'St. Gallen'), ('SH', 'Schaffhausen'),
        ('SO', 'Solothurn'), ('SZ', 'Schwyz'), ('TG', 'Thurgau'), ('TI', 'Tessin'),
        ('UR', 'Uri'), ('VD', 'Waadt'), ('VS', 'Wallis'), ('ZG', 'Zug'),
        ('ZH', 'Zürich'),
    ], validators=[Optional()])
    password = PasswordField('Passwort', validators=[
        DataRequired(), Length(min=8, message='Passwort muss mindestens 8 Zeichen lang sein.')
    ])
    password2 = PasswordField('Passwort bestätigen', validators=[
        DataRequired(), EqualTo('password', message='Passwörter stimmen nicht überein.')
    ])
    submit = SubmitField('Registrieren')


class LEGGründenForm(FlaskForm):
    name = StringField('Name der LEG', validators=[DataRequired(), Length(max=200)])
    beschreibung = TextAreaField('Beschreibung', validators=[Optional()])
    rechtsform = SelectField('Rechtsform', choices=[
        ('', '-- Bitte wählen --'),
        ('genossenschaft', 'Genossenschaft (empfohlen)'),
        ('verein', 'Verein'),
        ('einfache_gesellschaft', 'Einfache Gesellschaft'),
        ('ag', 'Aktiengesellschaft (AG)'),
        ('gmbh', 'GmbH'),
    ], validators=[DataRequired()])
    zweck = TextAreaField('Zweck der LEG', validators=[Optional()],
                          default='Gemeinsame Produktion, Speicherung und Verbrauch '
                                  'von lokal erzeugter erneuerbarer Energie.')
    einzugsgebiet = StringField('Einzugsgebiet', validators=[Optional(), Length(max=300)])
    adresse = StringField('Adresse', validators=[Optional(), Length(max=200)])
    plz = StringField('PLZ', validators=[Optional(), Length(max=10)])
    ort = StringField('Ort', validators=[DataRequired(), Length(max=100)])
    kanton = SelectField('Kanton', choices=[('', '-- Bitte wählen --')] + [
        ('AG', 'Aargau'), ('AI', 'Appenzell Innerrhoden'), ('AR', 'Appenzell Ausserrhoden'),
        ('BE', 'Bern'), ('BL', 'Basel-Landschaft'), ('BS', 'Basel-Stadt'),
        ('FR', 'Freiburg'), ('GE', 'Genf'), ('GL', 'Glarus'), ('GR', 'Graubünden'),
        ('JU', 'Jura'), ('LU', 'Luzern'), ('NE', 'Neuenburg'), ('NW', 'Nidwalden'),
        ('OW', 'Obwalden'), ('SG', 'St. Gallen'), ('SH', 'Schaffhausen'),
        ('SO', 'Solothurn'), ('SZ', 'Schwyz'), ('TG', 'Thurgau'), ('TI', 'Tessin'),
        ('UR', 'Uri'), ('VD', 'Waadt'), ('VS', 'Wallis'), ('ZG', 'Zug'),
        ('ZH', 'Zürich'),
    ], validators=[DataRequired()])
    anteilschein_betrag = FloatField('Anteilschein-Betrag (CHF)', validators=[Optional(), NumberRange(min=0)])
    min_anteilscheine = IntegerField('Min. Anteilscheine pro Mitglied', validators=[Optional(), NumberRange(min=1)],
                                     default=1)
    registrierung_offen = BooleanField('Mitglieder-Registrierung offen', default=True)
    submit = SubmitField('LEG gründen')


class LEGBearbeitenForm(LEGGründenForm):
    status = SelectField('Status', choices=[
        ('in_gründung', 'In Gründung'),
        ('gegründet', 'Gegründet'),
        ('aktiv', 'Aktiv'),
        ('aufgelöst', 'Aufgelöst'),
    ])
    gründungsdatum = DateField('Gründungsdatum', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Änderungen speichern')


class MitgliedBeitretenForm(FlaskForm):
    anzahl_anteilscheine = IntegerField('Anzahl Anteilscheine', validators=[
        DataRequired(), NumberRange(min=1)
    ], default=1)
    submit = SubmitField('Beitritt beantragen')
