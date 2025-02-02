import logging
import os
import secrets
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_migrate import Migrate
from geoip2.webservice import Client
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

# Fehlerbehandlung für Fehler 502, 404, 500
@app.errorhandler(502)
@app.errorhandler(404)
@app.errorhandler(500)
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

@app.after_request
def log_page_access(response):
    # Hier wird nach jeder Anfrage (Request) der Zugriffslog geschrieben
    if current_user.is_authenticated:
        access_logger.info(f"Page accessed: {request.path} by user {current_user.email}")
    else:
        access_logger.info(f"Page accessed: {request.path} by user Anonymous")
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
                # Benutzer ist gesperrt, Zeit abwarten
                remaining_lock_time = user.lock_time - datetime.utcnow()
                flash(f"Your account is locked. Please try again in {remaining_lock_time}.", 'danger')
                failed_login_logger.warning(f"Account locked for {email}, still within lock time.")
                return render_template('Anmeldung/login.html')

            # Überprüfen des Passworts
            if check_password_hash(user.password, password):
                login_logger.info(f"User {email} authenticated successfully!")
                login_user(user)
                user.failed_login_attempts = 0
                user.lock_time = None  # Sperre zurücksetzen
                db.session.commit()
                activity_logger.info(f"User {email} logged in successfully.")
                return redirect(url_for('dashboard'))
            else:
                # Passwort ist falsch, fehlerhaften Login-Zähler erhöhen
                user.failed_login_attempts += 1
                remaining_attempts = MAX_FAILED_ATTEMPTS - user.failed_login_attempts

                if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                    # Account sperren
                    user.lock_time = datetime.utcnow() + LOCK_TIME
                    db.session.commit()
                    failed_login_logger.warning(f"Account locked for {email} due to too many failed login attempts.")
                    flash(f"Too many failed login attempts. Your account is locked for {LOCK_TIME}.", 'danger')
                else:
                    db.session.commit()
                    failed_login_logger.warning(f"Failed login attempt with email: {email}")
                    flash(f'Invalid email or password. You have {remaining_attempts} attempt(s) left.', 'danger')

        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('Anmeldung/login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        birthdate = request.form.get('birthdate')  # Geburtsdatum als String vom Formular

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

        # Neues Benutzerobjekt erstellen und in der DB speichern
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, key=secrets.token_hex(16), geburtsdatum=datetime.strptime(birthdate, '%Y-%m-%d').date())
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

    return render_template('Dashboard/dashboard.html')

@app.route('/ai-projekt')
@login_required
def ai_projekt():
    return render_template('KI/ai-projekt.html')

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        # Logge den Logout-Ereignis
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
    reset_url = url_for('reset_password', token=token, _external=True)  # Generiere den Reset-Link

    msg = Message('Password Reset Request', recipients=[to_email], sender=os.getenv('MAIL_USERNAME'))  # Sender hinzufügen
    msg.body = f"""
    Hello,

    You requested a password reset. Please click the following link to reset your password:

    {reset_url}

    If you did not request a password reset, please ignore this email.

    Regards,
    Your Team
    """
    try:
        mail.send(msg)
        logging.info(f"Reset password email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
        flash('An error occurred while sending the reset email. Please try again later.', 'danger')

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
def update():
    return render_template('Test/Updates/updates.html')

@app.route('/Hilfe')
def hilfe():
    return render_template('FAQ/Hilfe.html')

@app.route('/bugs')
@login_required
def bugs_page():
    return render_template('Test/Bug/Bugs.html')

@app.route('/impressum')
def impressum():
    return render_template('Impressum/impressum.html')

@app.route('/Datenschutz')
def datenschutz():
    return render_template('DSGVO/Datenschutz.html')

@app.route('/Aurora-Ki')
def auroraKi():
    return send_from_directory('aurora-chat/public', 'index.html')

@app.route('/NB')
def nutzungsbedingungen():
    return render_template('Nutzungsbedingung/NB.html')

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
        return jsonify({"is_common": True, "message": "Das Passwort ist zu gängig und sollte vermieden werden!"}), 200  # OK-Antwort, aber mit einer Warnung

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

    # Verzeichnis für gespeicherte Formulardaten
    form_folder = 'form_data'
    if not os.path.exists(form_folder):
        try:
            os.makedirs(form_folder)
        except Exception as e:
            # Fehlerbehandlung beim Erstellen des Ordners
            return f"Fehler beim Erstellen des Ordners: {e}", 500

    # Speichern der Formulardaten in einer Textdatei
    try:
        with open(os.path.join(form_folder, 'submissions.txt'), 'a') as f:
            f.write(f"Name: {name}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Subject: {subject}\n")
            f.write(f"Message: {message}\n")
            f.write("-" * 40 + "\n")

    except Exception as e:
        return f"Fehler beim Speichern der Formulardaten: {e}", 500

    # Erfolgsnachricht und Weiterleitung
    flash("Thank you for your message. We will get back to you shortly (per Email).", 'success')
    return redirect(url_for('contact'))  # Zurück zur Kontaktseite

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tabellen erstellen
    app.run(debug=False)  #Debug-Modus explizit auf False setzen