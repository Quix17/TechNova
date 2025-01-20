import os
import secrets
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_mail import Mail, Message
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from blogposts import register_blogposts
from A_P_und_cp import check_password_requirements, load_common_passwords, is_common_password
from password_generator import generate_password
from models import db, User
from Editprofile import edit_profile

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

# SQLite-Datenbank konfigurieren
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisiere db mit Flask-App
db.init_app(app)

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

@login_manager.user_loader
def load_user(user_id):
    # Verwende db.session.get(), um den Benutzer anhand der ID zu laden
    return db.session.get(User, int(user_id))


# **Startseite**
@app.route('/')
def home():
    return render_template('Anmeldung/login.html')

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

        # Geburtsdatum umwandeln, wenn es im richtigen Format vorliegt
        try:
            geburtsdatum = datetime.strptime(birthdate, '%Y-%m-%d').date()  # Umwandlung in ein Date-Objekt
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('signup'))

        # Neues Benutzerobjekt erstellen und in der DB speichern
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, key=secrets.token_hex(16), geburtsdatum=geburtsdatum)
        db.session.add(new_user)
        db.session.commit()

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

@app.route('/Contact/')
def contact():
    return render_template('Contact/contact.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

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
def redirect_to_aurora():
    return redirect("http://localhost:3000", code=302)

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

        flash('Your password has been reset successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('Anmeldung/reset_password.html', token=token)

@app.route('/password_generator/<int:length>')
def password_generator(length):
    # Beispiel: Passwort mit gegebener Länge generieren
    password = generate_password(length)
    return jsonify({'password': password})


# In Progress Datei verlinken
@app.route('/Spaß_Projekt')
def spaß_projekt():
    return render_template('Test/Test/Spaß_Projekt.html')

@app.route('/updates')
def update():
    return render_template('Test/Updates/updates.html')

@app.route('/Hilfe')
def hilfe():
    return render_template('FAQ/Hilfe.html')

@app.route('/NB')
def nutzungsbedingungen():
    return render_template('Nutzungsbedingung/NB.html')

# Blueprint registrieren
app.register_blueprint(edit_profile, url_prefix='/edit_profile')

register_blogposts(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tabellen erstellen
    app.run(debug=True)