# LEG Portal Schweiz

Dieses Portal unterstützt die Gründung und den Betrieb von **Lokalen Energie Gemeinschaften (LEG)** in der Schweiz.

## Funktionen

- **Benutzer-Registrierung & Login** — Selbstregistrierung mit Schweizer Adressdaten
- **LEG gründen** — Wahl der Rechtsform (Genossenschaft, Verein, etc.), Angabe von Zweck, Einzugsgebiet und Anteilscheinen
- **Mitglieder-Selbstregistrierung** — Interessierte können einer offenen LEG beitreten
- **Mitgliederverwaltung** — Gründer/innen können Beitrittsanträge bestätigen oder ablehnen
- **Übersicht** — Alle aktiven und in Gründung befindlichen LEGs auf einen Blick

## Technologie

- **Python / Flask** — Web-Framework
- **SQLite** — Datenbank (keine externe DB nötig)
- **Bootstrap 5** — Responsive UI
- **Flask-Login** — Authentifizierung
- **Flask-WTF** — Formulare mit CSRF-Schutz

## Installation & Start

```bash
# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Anwendung starten
python run.py
```

Die Anwendung ist dann unter `http://localhost:5000` erreichbar.

## Projektstruktur

```
LEGPortal/
├── run.py                  # Einstiegspunkt
├── config.py               # Konfiguration
├── requirements.txt        # Python-Abhängigkeiten
├── app/
│   ├── __init__.py         # App-Factory
│   ├── models.py           # Datenbank-Modelle
│   ├── forms.py            # WTForms-Formulare
│   ├── routes/
│   │   ├── main.py         # Startseite, Info
│   │   ├── auth.py         # Login, Registrierung, Profil
│   │   ├── leg.py          # LEG gründen, bearbeiten, anzeigen
│   │   └── members.py      # Beitreten, Mitgliederverwaltung
│   └── templates/          # Jinja2 HTML-Templates
└── instance/               # SQLite-Datenbank (auto-erstellt)
```
