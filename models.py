from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=True)
    key = db.Column(db.String(100), nullable=False)
    reset_token = db.Column(db.String(100), nullable=True)
    geburtsdatum = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

    # Diese Methode hinzufügen
    @property
    def is_active(self):
        # Rückgabewert für aktiven Benutzer. Wenn du auch eine Logik für inaktive Benutzer hast,
        # kannst du hier entsprechende Bedingungen einfügen.
        return True