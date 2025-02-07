from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    key = db.Column(db.String(100), nullable=False)
    reset_token = db.Column(db.String(100), nullable=True)
    geburtsdatum = db.Column(db.Date, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    login_attempts_today = db.Column(db.Integer, default=0)  # Anzahl der Login-Versuche an diesem Tag
    last_login_attempt_date = db.Column(db.Date, nullable=True)  # Tag des letzten erfolgreichen Logins
    total_login_attempts = db.Column(db.Integer, default=0)  # Gesamte erfolgreiche Logins
    lock_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Zeit der Kontoerstellung
    last_login = db.Column(db.DateTime, nullable=True)  # Letztes Login
    last_ip = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)  # User-Agent
    captcha_verified = db.Column(db.Boolean, default=False)  # CAPTCHA verifiziert (für Botschutz)
    account_locked = db.Column(db.Boolean, default=False)  # Flag, ob der Account gesperrt wurde

    def __repr__(self):
        return f'<User {self.email}>'

    @property
    def is_active(self):
        return not self.account_locked  # Aktiv nur, wenn nicht gesperrt