import os
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from authlib.integrations.flask_client import OAuth
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_mail import Mail, Message
import re

# Passwortgenerierung importieren
from password_generator import generate_password

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

# SQLite-Datenbank konfigurieren
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Migration mit Flask-Migrate einrichten
migrate = Migrate(app, db)

# Authlib OAuth
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    authorize_url=f'https://{os.getenv("AUTH0_DOMAIN")}/authorize',
    authorize_params=None,
    access_token_url=f'https://{os.getenv("AUTH0_DOMAIN")}/oauth/token',
    refresh_token_url=f'https://{os.getenv("AUTH0_DOMAIN")}/oauth/token',
    client_kwargs={'scope': 'openid profile email'},
)

# Mail Setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

# User Model für Login/Registrierung
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=True)  # Passwort für reguläre Anmeldung
    key = db.Column(db.String(100), nullable=False)
    reset_token = db.Column(db.String(100), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Passwortanforderungen
def check_password_requirements(password):
    # Mindestens 26 Zeichen
    length_check = len(password) >= 26
    # Mindestens 5 Großbuchstaben
    uppercase_check = len(re.findall(r'[A-Z]', password)) >= 5
    # Mindestens 2 Zahlen
    number_check = len(re.findall(r'\d', password)) >= 2
    # Mindestens 2 Sonderzeichen
    special_check = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password)) >= 2

    # Rückgabe der Ergebnisse der Passwortanforderungen
    return length_check, uppercase_check, number_check, special_check

# Route zum Generieren eines Passworts mit der gewünschten Länge
@app.route('/password_generator/<int:length>', methods=['GET'])
def password_generator(length):
    # Überprüfen, ob die Länge zwischen 12 und 64 liegt
    if length < 12 or length > 64:
        return jsonify({'error': 'Password length must be between 12 and 64 characters'}), 400

    # Passwort mit der angegebenen Länge generieren
    password = generate_password(length)

    # Rückgabe des generierten Passworts als JSON
    return jsonify({'password': password})

# Funktion zum Laden häufiger Passwörter
def load_common_passwords(file_path):
    try:
        with open(file_path, 'r') as f:
            common_passwords = set(line.strip().lower() for line in f)
        return common_passwords
    except FileNotFoundError:
        print("Die Datei mit den häufigen Passwörtern wurde nicht gefunden.")
        return set()

# Der Pfad zur Datei mit den häufigen Passwörtern
common_password_file = './static/txt/common_passwords.txt'
common_passwords = load_common_passwords(common_password_file)

# Funktion zum Überprüfen von häufigen Passwörtern
def is_common_password(password):
    return password.lower() in common_passwords

# **Startseite**
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Debugging: Überprüfen, ob die Formulardaten korrekt sind
        print(f"Login attempt with email: {email}")

        # Überprüfen, ob der Benutzer existiert
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            print(f"User {email} authenticated successfully!")
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            print("Invalid email or password.")
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('signup'))

        # Überprüfen, ob die E-Mail bereits existiert
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'danger')
            return redirect(url_for('signup'))

        # Überprüfen, ob das Passwort die Anforderungen erfüllt
        length_check, uppercase_check, number_check, special_check = check_password_requirements(password)

        if not (length_check and uppercase_check and number_check and special_check):
            flash(
                'Password does not meet the requirements: at least 26 characters, 5 uppercase letters, 2 numbers, and 2 special characters.',
                'danger')
            return redirect(url_for('signup'))

        # Überprüfen, ob das Passwort häufig ist
        if is_common_password(password):
            flash('Password is too common. Please choose a stronger password.', 'danger')
            return redirect(url_for('signup'))

        # Neues Benutzerobjekt erstellen und in der DB speichern
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, key=secrets.token_hex(16))
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/auth0_login')
def auth0_login():
    # Benutzer umleiten, um sich bei Auth0 anzumelden
    redirect_uri = url_for('auth0_callback', _external=True)
    return auth0.authorize_redirect(redirect_uri)

@app.route('/auth0_callback')
def auth0_callback():
    token = auth0.authorize_access_token()
    if token:
        user = auth0.parse_id_token(token)
        if user:
            print("Authenticated user:", user)
            email = user.get('email')
            existing_user = User.query.filter_by(email=email).first()

            if not existing_user:
                print(f"New user detected: {email}. Creating user.")
                new_user = User(email=email, key=secrets.token_hex(16))
                db.session.add(new_user)
                db.session.commit()
                existing_user = new_user

            login_user(existing_user)
            return redirect(url_for('dashboard'))
        else:
            print("Failed to parse user data.")
            flash('Authentication failed. Please try again.', 'danger')
            return redirect(url_for('home'))
    else:
        print("No token received from Auth0.")
        flash('Authentication failed. Please try again.', 'danger')
        return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        entered_key = request.form.get('key')
        if entered_key == current_user.key:
            return "Access Granted!"
        else:
            flash("Invalid Key!", "danger")

    return render_template('dashboard.html')

@app.route('/ai-projekt')
@login_required
def ai_projekt():
    return render_template('ai-projekt.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        # Benutzer nach der E-Mail suchen
        user = User.query.filter_by(email=email).first()
        if user:
            # Generiere einen Reset-Token und speichere ihn
            reset_token = secrets.token_urlsafe(16)
            user.reset_token = reset_token
            db.session.commit()

            # E-Mail mit Reset-Token versenden
            send_reset_email(user.email, reset_token)
            flash('Password reset email sent. Please check your inbox.', 'info')
        else:
            flash('Email not found.', 'danger')

    return render_template('forgot_password.html')

def send_reset_email(to_email, token):
    msg = Message('Password Reset Request', recipients=[to_email])
    msg.body = f'Here is your password reset token: {token}'
    mail.send(msg)

#Bearbeiten des Profils
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Die Passwörter stimmen nicht überein!', 'danger')
            return redirect(url_for('edit_profile'))

        if new_password:
            hashed_password = generate_password_hash(new_password)
            current_user.password = hashed_password

        if new_email:
            current_user.email = new_email

        db.session.commit()
        flash('Profil erfolgreich aktualisiert!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_profile.html')

#Löschen des Profils
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Konto erfolgreich gelöscht.', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tabellen erstellen
    # Automatisch das Passwort beim Starten generieren
    print(generate_password(32))  # Beispiel für die Passwortgenerierung
    app.run(debug=True)