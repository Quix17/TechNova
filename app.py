import json
import logging
import os
import secrets
from datetime import timedelta, date
from logging.handlers import RotatingFileHandler
from flask_cors import cross_origin

from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_migrate import Migrate
from geoip2.webservice import Client
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

from A_P_und_cp import check_password_requirements, is_common_password, common_passwords
from Editprofile import edit_profile
from blogposts import register_blogposts
from models import db, User
from password_generator import generate_password

# Verzeichnis für Logs erstellen
log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Setup für Flask-Anwendung
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

# Setze Flask auf Produktionsmodus
app.config['FLASK_ENV'] = 'production'
app.config['DEBUG'] = False

# SQLite-Datenbank konfigurieren
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisiere db mit Flask-App
db.init_app(app)

login_manager = LoginManager(app)

# Migration mit Flask-Migrate einrichten
migrate = Migrate(app, db)

# Erstelle Client mit deinem GeoIP-Zugriffsschlüssel
geoip_client = Client(account_id='your_account_id', license_key='your_license_key')

# Logger für verschiedene Protokolle konfigurieren
def create_logger(log_name, log_file, level=logging.INFO):
    logger = logging.getLogger(log_name)
    handler = RotatingFileHandler(os.path.join(log_folder, log_file), maxBytes=10 * 1024 * 1024, backupCount=5)
    handler.setLevel(level)  # Hier den richtigen Level setzen
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Erstelle verschiedene Logger
email_change_logger = create_logger('email_change_logger', 'email_change_log.log')
login_logger = create_logger('login_logger', 'login.log')
error_logger = create_logger('error_logger', 'error.log', logging.ERROR)
access_logger = create_logger('access_logger', 'access.log')
activity_logger = create_logger('activity_logger', 'activity.log')
signup_logger = create_logger('signup_logger', 'signup.log')
logout_logger = create_logger('logout_logger', 'logout.log', logging.INFO)
password_change_logger = create_logger('password_change_logger', 'password_change.txt', logging.INFO)
password_reset_logger = create_logger('password_reset_logger', 'password_reset.log')
failed_login_logger = create_logger('failed_login_logger', 'failed_login.log')
account_deletion_logger = create_logger('account_deletion_logger', 'account_deletion.txt', logging.INFO)
user_action_logger = create_logger('user_action_logger', 'user_action.log', logging.INFO)
user_error_logger = create_logger('user_error_logger', 'user_error.log', logging.ERROR)

# Fehlerbehandlung für Fehler 400, 401, 403, 404, 500, 502, 501
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(502)
@app.errorhandler(501)
def handle_error(error):
    user_ip = request.remote_addr  # IP-Adresse des Benutzers
    ray_id = secrets.token_hex(8)  # Zufällige Ray-ID
    error_code = error.code if hasattr(error, 'code') else 500  # Fehlercode
    method = request.method  # HTTP-Methode
    current_user_info = "Anonymer Benutzer"

    # Prüfen, ob ein Benutzer eingeloggt ist
    if current_user.is_authenticated:
        current_user_info = f"Benutzer ID: {current_user.id}, E-Mail: {current_user.email}"

    # Fehlerdetails sammeln
    location = "Unbekannt"
    try:
        geo_response = geoip_client.insights(user_ip)
        location = f"{geo_response.city.name}, {geo_response.country.name}"
    except Exception:
        pass  # Wenn keine GeoIP-Informationen verfügbar sind, bleibt es "Unbekannt"

    # Header-Informationen sammeln
    headers = request.headers
    user_agent = headers.get('User-Agent', 'Unbekannt')
    referer = headers.get('Referer', 'Unbekannt')
    accept_language = headers.get('Accept-Language', 'Unbekannt')

    # Wenn Referer leer ist oder blockiert wurde, füge es als besonderen Fall hinzu
    if not referer or referer == 'Unbekannt':
        referer = "Referer-Header wurde nicht gesendet oder blockiert."

    # GET- und POST-Parameter sammeln
    get_params = request.args if request.args else "Keine GET-Parameter"
    post_params = request.form if request.method == 'POST' else "Keine POST-Daten"

    # Session- und Cookie-Daten
    session_data = session.sid if hasattr(session, 'sid') else "Keine Session"
    cookies = request.cookies if request.cookies else "Keine Cookies"

    # Fehlermeldung und Stacktrace
    error_message = str(error)

    # Log-Nachricht erstellen
    log_message = (
        f"Fehler {error_code} | IP: {user_ip} | Ray ID: {ray_id} | Path: {request.path} | "
        f"Methode: {method} | Location: {location} | {current_user_info} | "
        f"User-Agent: {user_agent} | Referer: {referer} | Accept-Language: {accept_language} | "
        f"GET-Parameter: {get_params} | POST-Daten: {post_params} | "
        f"Session-ID: {session_data} | Cookies: {cookies} | Fehlermeldung: {error_message}"
    )

    # Fehler in die Logdatei schreiben
    error_logger.error(log_message)
    error_logger.error("\n" + "-" * 50 + "\n")  # Trenner nach jeder Log-Nachricht

    # Benutzerfreundliche Fehlerseite anzeigen
    return render_template(
        'Fehlerseite/fehler.html',
        ray_id=ray_id,
        ip=user_ip,
        error_code=error_code,
        location=location,
        user=current_user_info,
        method=method,
        get_params=get_params,
        post_params=post_params,
        session_data=session_data,
        cookies=cookies,
        user_agent=user_agent,
        referer=referer,
        accept_language=accept_language
    ), error_code

# Setze den Log-Level für alle Logger auf INFO
login_logger.setLevel(logging.INFO)
error_logger.setLevel(logging.INFO)
access_logger.setLevel(logging.INFO)
activity_logger.setLevel(logging.INFO)
failed_login_logger.setLevel(logging.INFO)
email_change_logger.setLevel(logging.INFO)
logout_logger.setLevel(logging.INFO)
password_change_logger.setLevel(logging.INFO)
password_reset_logger.setLevel(logging.INFO)
signup_logger.setLevel(logging.INFO)
account_deletion_logger.setLevel(logging.INFO)

# Setze den Log-Level des Flask-Loggers auf INFO
app.logger.setLevel(logging.INFO)

# Setze den Log-Level für den Werkzeug-Logger auf INFO
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

from datetime import datetime

@app.after_request
def log_page_access(response):
    # Liste von Routen, die nicht geloggt werden sollen
    excluded_routes = [
        "/check-cookies-acceptance",
        "/some-other-route",  # Weitere Routen hinzufügen, die nicht geloggt werden sollen
    ]

    # Prüfen, ob der angeforderte Pfad in der Liste der auszuschließenden Routen ist
    if request.path in excluded_routes:
        return response  # Keine Log-Nachricht für diese Routen

    # Prüfen, ob die Anfrage zu einer statischen Datei gehört
    if "/static/" in request.path:
        return response  # Keine Log-Nachricht für statische Dateien

    # Logge den Zugriff im benutzerdefinierten Format
    # Prüfen, ob die Anfrage eine POST-Anfrage ist
    if request.method == 'POST':
        if current_user.is_authenticated:
            access_logger.info(f"Page accessed: {request.path} by user {current_user.email} with POST method")
        else:
            access_logger.info(f"Page accessed: {request.path} by user Anonymous with POST method")
    else:
        if current_user.is_authenticated:
            access_logger.info(f"Page accessed: {request.path} by user {current_user.email} with {request.method} method")
        else:
            access_logger.info(f"Page accessed: {request.path} by user Anonymous with {request.method} method")


    # Content-Security-Policy Header setzen
    csp_policy = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://ajax.googleapis.com https://assets.codepen.io https://unpkg.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; img-src 'self' data: http://127.0.0.1:5000 https://127.0.0.1:5000 https://via.placeholder.com; font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; connect-src 'self' http://localhost:5000; frame-ancestors 'none'; object-src 'none';"
    response.headers['Content-Security-Policy'] = csp_policy

    return response

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

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# **Startseite**
@app.route('/')
def home():
    access_logger.info(f"Page accessed: {request.path}")
    return render_template('Anmeldung/login.html')

MAX_FAILED_ATTEMPTS = 5
LOCK_TIME = timedelta(minutes=15)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        login_logger.info(f"Login attempt with email: {email}")

        user = User.query.filter_by(email=email).first()

        if user:
            # Prüfen, ob der Account gesperrt ist
            if user.lock_time and datetime.utcnow() < user.lock_time:
                remaining_lock_time = user.lock_time - datetime.utcnow()
                flash(f"Your account is locked. Please try again in {remaining_lock_time}.", 'danger')
                failed_login_logger.warning(f"Account locked for {email}, still within lock time.")
                return render_template('Anmeldung/login.html')

            # Überprüfen des Passworts
            if check_password_hash(user.password, password):
                login_logger.info(f"User {email} authenticated successfully!")

                # Prüfe, ob ein neuer Tag angebrochen ist, und setze `login_attempts_today` falls nötig zurück
                today_date = datetime.utcnow().date()
                if user.last_login_attempt_date != today_date:
                    user.login_attempts_today = 0  # Zurücksetzen auf 0 für einen neuen Tag

                # Tages- und Gesamtlaufzähler aktualisieren
                user.login_attempts_today += 1  # Erhöhe die täglichen Anmeldeversuche
                user.total_login_attempts += 1  # Erhöhe die Gesamtanzahl der Logins
                user.last_login_attempt_date = today_date  # Aktualisiere das Datum des letzten Logins

                # IP-Adresse und User-Agent setzen
                ip_address = request.headers.get('X-Forwarded-For') or request.remote_addr or "0.0.0.0"
                user_agent = request.headers.get('User-Agent') or "Unknown User-Agent"

                # Weitere Benutzer-Login-Informationen aktualisieren
                user.last_login = datetime.utcnow()
                user.last_ip = ip_address
                user.user_agent = user_agent
                user.failed_login_attempts = 0
                user.lock_time = None

                # Daten speichern
                try:
                    db.session.commit()
                    login_logger.info(
                        f"Database commit successful for user {email}. IP: {user.last_ip}, User-Agent: {user.user_agent}")
                except Exception as e:
                    error_logger.error(f"Database commit failed for user {email}. Error: {str(e)}")
                    flash("An error occurred while saving your login details. Please try again later.", "danger")
                    return render_template("Anmeldung/login.html")

                # Benutzer anmelden
                login_user(user)
                activity_logger.info(
                f"User {email} logged in successfully from IP: {user.last_ip} with User-Agent: {user.user_agent}")
                return redirect(url_for('dashboard', user_id=user.id))

            else:
                # Berechnung für einen fehlgeschlagenen Login
                user.failed_login_attempts += 1
                remaining_attempts = MAX_FAILED_ATTEMPTS - user.failed_login_attempts

                # Account sperren, wenn fehlgeschlagene Versuche überschritten werden
                if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                    user.lock_time = datetime.utcnow() + LOCK_TIME
                    db.session.commit()
                    flash(f"Too many failed login attempts. Your account is locked for {LOCK_TIME}.", 'danger')
                    failed_login_logger.warning(f"Account locked for {email} due to too many failed login attempts.")
                else:
                    db.session.commit()
                    flash(f'Invalid email or password. You have {remaining_attempts} attempt(s) left.', 'danger')

                return render_template("Anmeldung/login.html")
        else:
            login_logger.warning(f"Login attempt failed: No user found with email {email}.")
            flash("Invalid email or password. Please try again.", 'danger')
            return render_template("Anmeldung/login.html")

    # GET-Request: Einfach nur die Login-Seite anzeigen
    return render_template('Anmeldung/login.html')


from datetime import datetime, date

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        birthdate_str = request.form.get('birthdate')  # Geburtsdatum als String vom Formular

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('signup'))

        # Überprüfen, ob die E-Mail bereits existiert
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'danger')
            return redirect(url_for('signup'))

        # Passwortanforderungen prüfen
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

        # Geburtsdatum validieren
        try:
            birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            today = date.today()

            # Sicherstellen, dass das Geburtsdatum in der Vergangenheit liegt
            if birthdate > today:
                flash('Birthdate cannot be in the future.', 'danger')
                return redirect(url_for('signup'))

            # Alter berechnen
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

            if age < 18:
                flash('You must be at least 18 years old to sign up.', 'danger')
                return redirect(url_for('signup'))
            if age > 90:
                flash('Maximum age for sign up is 90 years.', 'danger')
                return redirect(url_for('signup'))

        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('signup'))

        # Neues Benutzerobjekt erstellen und in der DB speichern
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, key=secrets.token_hex(16), geburtsdatum=birthdate)
        db.session.add(new_user)
        db.session.commit()

        signup_logger.info(f"New user signed up: {email}")
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('Anmeldung/signup.html')


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
            logging.info(f"Auth0 login successful for user: {email}")
            return redirect(url_for('dashboard', user_id=user.i))
        else:
            print("Failed to parse user data.")
            flash('Authentication failed. Please try again.', 'danger')
            return redirect(url_for('home'))
    else:
        print("No token received from Auth0.")
        flash('Authentication failed. Please try again.', 'danger')
        return redirect(url_for('home'))


@app.route('/dashboard_id<int:user_id>', methods=['GET', 'POST'])
@login_required  # Sicherstellen, dass der Benutzer eingeloggt ist
def dashboard(user_id):
    # Debugging: Überprüfen, ob der Benutzer eingeloggt ist
    if not current_user.is_authenticated:
        flash("Du bist nicht eingeloggt! Bitte logge dich ein, um auf das Dashboard zuzugreifen.", "danger")
        return redirect(url_for('login'))  # Stelle sicher, dass der Benutzer eingeloggt ist

    # Sicherstellen, dass der angeforderte user_id dem aktuell eingeloggten Benutzer entspricht
    if user_id != current_user.id:
        flash("Du hast keinen Zugriff auf dieses Dashboard.", "danger")
        return redirect(url_for('login'))  # Falls der User-ID nicht übereinstimmt, zurück zum Login

    if request.method == 'POST':
        entered_key = request.form.get('key')
        if entered_key == current_user.key:
            flash("Access Granted!", "success")
            return render_template('Dashboard/dashboard.html')
        else:
            flash("Invalid Key!", "danger")

    # Übergabe der user_id an das Template
    return render_template('Dashboard/dashboard.html', user_id=current_user.id)



@app.route('/ai-projekt')
@login_required
def ai_projekt():
    return render_template('KI/ai-projekt.html')

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_logger.info(f"User {current_user.email} logged out.")  # Hier wird der logout_logger verwendet

    logout_user()  # Der Benutzer wird abgemeldet
    flash('Du wurdest erfolgreich abgemeldet.', 'success')
    return redirect(url_for('login'))  # Nach dem Logout zurück zur Login-Seite

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

            # Sende E-Mail mit Reset-Link
            send_reset_email(user.email, reset_token)
            flash('An email has been sent with the password reset token.', 'info')
        else:
            flash('Email address not found.', 'danger')

    return render_template('Anmeldung/forgot_password.html')

def send_reset_email(to_email, token):
    reset_url = url_for('reset_password', token=token, _external=True)

    # Lese das HTML-Template von der Datei
    with open('templates/email/password_email.html', 'r', encoding='utf-8') as file:
        template = file.read()

    # Ersetze den Platzhalter mit der Reset-URL
    html_content = template.replace('{reset_url}', reset_url)

    # Verwende die E-Mail-Adresse, die bei forgot_password eingegeben wurde, als Sender
    sender_email = to_email

    # Erstelle die E-Mail-Nachricht
    msg = Message(
        'Password Reset Request',
        recipients=[to_email],
        sender=sender_email,
        html=html_content,
    )

    # Textversion für E-Mail-Clients, die kein HTML unterstützen
    msg.body = f"""
    Hello,

    You requested a password reset. Please click the following link to reset your password:

    {reset_url}

    If you did not request a password reset, please ignore this email.

    This link will expire in 24 hours.

    Best regards,
    Your Team
    """

    try:
        mail.send(msg)
        logging.info(f"Reset password email sent to {to_email} with sender {sender_email}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise Exception('An error occurred while sending the reset email.')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('reset_password', token=token))

        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password
        user.reset_token = None  # Token zurücksetzen, nachdem das Passwort geändert wurde
        db.session.commit()

        # Logging der Passwortänderung
        password_change_logger.info(f"User {user.email} changed their password.")

        flash('Your password has been reset successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('Anmeldung/reset_password.html', token=token)

@app.route('/password_generator/<int:length>')
def password_generator(length):
    # Beispiel: Passwort mit gegebener Länge generieren
    password = generate_password(length)
    return jsonify({'password': password})

@app.route('/updates')
@login_required
def update():
    return render_template('Test/Updates/updates.html')

@app.route('/Hilfe')
def hilfe():
    return render_template('FAQ/Hilfe.html')

@app.route('/bugs')
@login_required
def bugs_page():
    return render_template('Test/Bug/Bugs.html')

@app.route('/meer')
@login_required
def meer():
    return render_template('Meer/meer.html')

@app.route('/impressum')
def impressum():
    return render_template('Impressum/impressum.html')

@app.route('/Datenschutz')
def datenschutz():
    return render_template('DSGVO/Datenschutz.html')

@app.route('/Aurora-Ki')
@login_required
def auroraKi():
    return send_from_directory('aurora-chat/public', 'index.html')

@app.route('/NB')
def nutzungsbedingungen():
    return render_template('Nutzungsbedingung/NB.html')

@app.route('/backup_codes')
@login_required
def backup_codes():
    return render_template('Anmeldung/backup_codes.html')

# Blueprint registrieren
app.register_blueprint(edit_profile, url_prefix='/edit_profile')

register_blogposts(app)

@app.route('/password_checker', methods=['POST'])
def check_password():
    try:
        data = request.get_json()
        password = data.get('password')
    except Exception as e:
        return jsonify({"message": "Ungültige Anfrage, JSON erwartet!"}), 400

    if not password:
        return jsonify({"message": "Passwort darf nicht leer sein!"}), 400

    # Überprüfe, ob das Passwort in der Liste häufiger Passwörter ist
    if password.lower() in common_passwords:
        return jsonify({"is_common": True, "message": "Passwort ist zu gängig!"}), 200  # OK-Antwort, aber mit einer Warnung

    return jsonify({"is_common": False, "message": "Das Passwort ist sicher."}), 200  # OK-Antwort bei sicherem Passwort

@app.route('/Contact/')
def contact():
    return render_template('Contact/contact.html')


@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    # Formulardaten empfangen
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Benutzerbezogene Daten
    user_ip = request.remote_addr  # IP-Adresse des Benutzers
    user_id = current_user.id if current_user.is_authenticated else 'Anonym'
    username = current_user.email if current_user.is_authenticated else 'Unbekannt'  # Benutzername (oder Anonym)
    user_agent = request.headers.get('User-Agent', 'Unbekannt')  # User-Agent des Benutzers
    referer = request.headers.get('Referer', 'Unbekannt')  # Referer (woher die Anfrage kam)
    session_data = session.sid if hasattr(session, 'sid') else 'Keine Session'  # Session ID

    # Aktuelles Datum und Uhrzeit
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Verzeichnis für gespeicherte Formulardaten
    form_folder = 'form_data'
    if not os.path.exists(form_folder):
        try:
            os.makedirs(form_folder)
        except Exception as e:
            flash(f"Fehler beim Erstellen des Ordners: {e}", 'danger')
            return redirect(url_for('contact'))

    # Detaillierte Logging-Nachricht (mit strukturierter Formatierung)
    log_message = (
        f"\n**EINGEREICHTE DATEN (am {timestamp})**\n"
        f"===============================\n"
        f"**Name:** {name}\n"
        f"**Email:** {email}\n"
        f"**Betreff:** {subject}\n"
        f"**Nachricht:**\n{message}\n\n"

        f"**BENUTZERINFORMATIONEN**\n"
        f"===========================\n"
        f"**Benutzername:** {username}\n"
        f"**User ID:** {user_id}\n"
        f"**IP-Adresse:** {user_ip}\n"
        f"**User-Agent:** {user_agent}\n"
        f"**Referer:** {referer}\n"
        f"**Session ID:** {session_data}\n\n"

        f"{'=' * 40}\n\n"
        f"{'=' * 40}\n\n"
    )

    # Weitere Benutzerdaten und Aktionen loggen
    user_action_logger.info(f"Benutzeraktionen: {log_message}")

    try:
        # Speichern der Formulardaten in einer Textdatei
        with open(os.path.join(form_folder, 'submissions.txt'), 'a') as f:
            f.write(log_message)

        # Erfolgsprotokollierung
        success_message = f"Formular erfolgreich übermittelt von Benutzer {username} ({user_id}) (IP: {user_ip})"
        user_action_logger.info(success_message)

    except Exception as e:
        # Fehler beim Speichern der Formulardaten
        error_message = f"Fehler beim Speichern der Formulardaten für Benutzer {username} ({user_id}): {e}"
        user_error_logger.error(error_message)  # Fehler loggen
        flash(f"Fehler beim Speichern der Formulardaten: {e}", 'danger')
        return redirect(url_for('contact'))

    # Erfolgsnachricht
    flash("Vielen Dank für Ihre Nachricht. Wir werden uns in Kürze bei Ihnen melden, per E-Mail.", 'success')
    return redirect(url_for('contact'))


@app.route('/save_backup_codes', methods=['POST'])
def save_backup_codes():
    try:
        data = request.get_json()  # Empfange die Daten als JSON
        user_id = data.get('user_id')  # Benutzer-ID extrahieren
        codes = data.get('codes')  # Backup-Codes extrahieren

        # Überprüfen, ob die notwendigen Daten vorhanden sind
        if not user_id or not codes:
            return jsonify({"success": False, "message": "Benutzer-ID oder Codes fehlen."})

        # Benutzer anhand der user_id finden
        user = User.query.get(user_id)

        # Wenn der Benutzer nicht existiert, eine Fehlermeldung zurückgeben
        if not user:
            return jsonify({"success": False, "message": "Benutzer nicht gefunden."})

    
        # Speichern der Backup-Codes im Benutzer-Objekt
        user.backup_codes = codes
        db.session.commit()  # Änderungen in der DB speichern

        return jsonify({"success": True, "message": "Backup-Codes wurden erfolgreich gespeichert."})

    except Exception as e:
        print(f"Fehler beim Speichern der Backup-Codes: {e}")
        return jsonify({"success": False, "message": f"Fehler beim Speichern der Backup-Codes: {str(e)}"})


@app.route('/check_backup_codes/<int:user_id>', methods=['GET'])
def check_backup_codes(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            print(f"Benutzer mit ID {user_id} nicht gefunden.")
            return jsonify({"success": False, "message": "Benutzer nicht gefunden."})

        codesExist = user.backup_codes is not None
        print(f"Benutzer mit ID {user_id} hat Backup-Codes: {codesExist}")

        return jsonify({"success": True, "codesExist": codesExist})

    except Exception as e:
        print(f"Fehler beim Prüfen der Backup-Codes: {e}")
        return jsonify({"success": False, "message": f"Fehler beim Prüfen der Backup-Codes: {str(e)}"})

@app.route('/login_with_backup', methods=['GET'])
def login_with_backup_form():
    # Diese Route rendert das Formular für die Eingabe des Backup-Codes
    return render_template('Anmeldung/backup_codes.html')  # Verweis auf die HTML-Datei mit dem Formular

@app.route('/login_with_backup', methods=['POST'])
def login_with_backup():
    try:
        # JSON-Daten abrufen
        data = request.get_json(force=True)

        if not data:
            raise ValueError("Bitte füllen Sie alle Felder aus.")

        email = data.get('email')
        backup_code = data.get('backup_code')

        if not email or not backup_code:
            raise ValueError("Benutzer oder Backup-Code ungültig.")  # Einheitliche Fehlermeldung

        user = User.query.filter_by(email=email).first()

        # Sicherheit: Einheitliche Fehlermeldung, egal ob User existiert oder nicht
        if not user or not user.backup_codes or backup_code not in user.backup_codes:
            raise ValueError("Benutzer oder Backup-Code ungültig.")  # Angreifer kriegt keine Infos

        if user.backup_codes[backup_code]['used']:
            raise ValueError("Benutzer oder Backup-Code ungültig.")  # Gleiche Meldung für verbrauchten Code

        # Backup-Code als verwendet markieren und speichern
        user.backup_codes[backup_code]['used'] = True
        backup_codes_json = json.dumps(user.backup_codes)
        db.session.execute(
            text("UPDATE user SET backup_codes = :backup_codes WHERE email = :email"),
            {"backup_codes": backup_codes_json, "email": email}
        )
        db.session.commit()
        login_user(user)

        return jsonify({
            "status": "success",
            "message": "Login erfolgreich! Willkommen im Dashboard.",
            "user_id": user.id
        }), 200

    except ValueError:
        return jsonify({"status": "error", "message": "Benutzer oder Backup-Code ungültig."}), 400  # Einheitliche Meldung

    except Exception:
        return jsonify({"status": "error", "message": "Ein unerwarteter Fehler ist aufgetreten."}), 500


@app.route('/get_backup_code_info', methods=['GET'])
def get_backup_code_info():
    # Hole den Benutzer aus der Datenbank
    user = User.query.get(current_user.id)
    
    # Gib die Anzahl der generierten Codes und den Zeitpunkt der letzten Generierung zurück
    return jsonify({
        'backup_code_generation_count': user.backup_code_generation_count,
        'last_backup_code_generation': user.last_backup_code_generation.isoformat() if user.last_backup_code_generation else None
    })


@app.route('/get_remaining_timeout', methods=['GET'])
def get_remaining_timeout():
    # Hole den Benutzer aus der Datenbank
    user = User.query.get(current_user.id)
    
    # Berechne den verbleibenden Timeout
    if user.last_backup_code_generation:
        last_generated = user.last_backup_code_generation
        time_diff = datetime.utcnow() - last_generated
        timeout_in_hours = (user.backup_code_generation_count + 1) * 24  # 24h, 48h, 72h
        remaining_time = timeout_in_hours - time_diff.total_seconds() / 3600
    else:
        remaining_time = 0  # Kein Timeout, falls noch nie generiert

    user.remaining_timeout = max(0, remaining_time)  # Speichert die verbleibende Zeit, keine negative Werte
    db.session.commit()

    return jsonify({'remaining_timeout': max(0, remaining_time)})


@app.route('/update_backup_code_info', methods=['POST'])
def update_backup_code_info():
    # Hole den Benutzer aus der Datenbank
    user = User.query.get(current_user.id)
    
    # Erhöhe die Generierungsanzahl und setze das aktuelle Datum
    user.backup_code_generation_count += 1
    user.last_backup_code_generation = datetime.utcnow()
    
    # Berechne die Wartezeit basierend auf der Generierungsanzahl (in Stunden)
    timeout_in_hours = (user.backup_code_generation_count + 1) * 24
    user.remaining_timeout = timeout_in_hours
    
    # Speichere die Änderungen
    db.session.commit()

    return jsonify({'success': True})


@app.route('/check-cookies-acceptance', methods=['POST'])
@cross_origin()  # Nur diese Route erlaubt CORS
def check_cookies_acceptance():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"message": "Fehler beim Abrufen der Daten"}), 500

    user_id = data.get('userId')

    if not user_id:
        return jsonify({"message": "Benutzer ID nicht gefunden"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Benutzer nicht gefunden"}), 404

    # Gibt den aktuellen Wert von cookies_accepted zurück (True, False oder None)
    return jsonify({"cookiesAccepted": user.cookies_accepted}), 200


@app.route('/save-cookies-acceptance', methods=['POST'])
@cross_origin()  # Nur diese Route erlaubt CORS
def save_cookies_acceptance():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"message": "Fehler beim Abrufen der Daten"}), 500

    user_id = data.get('userId')
    cookies_accepted = data.get('cookiesAccepted')

    if cookies_accepted is None:
        return jsonify({"message": "Fehler: cookiesAccepted ist None"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Benutzer nicht gefunden"}), 404

    cookies_value = "true" if cookies_accepted else "false"

    try:
        user.cookies_accepted = cookies_value
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Fehler beim Speichern der Zustimmung: {str(e)}"}), 500

    return jsonify({"message": "Zustimmung erfolgreich gespeichert"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tabellen erstellen
    app.run(debug=False)  #Debug-Modus explizit auf False setzen