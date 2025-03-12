import logging
import os
import re

from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash

from models import db, User

# Blueprint erstellen
edit_profile = Blueprint('edit_profile', __name__)

# Erstellen eines allgemeinen Log-Ordners, falls er nicht existiert
log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Logger für E-Mail-Änderungen, Passwortänderungen und Konto löschen
email_change_logger = logging.getLogger('email_change_logger')
password_change_logger = logging.getLogger('password_change_logger')
account_deletion_logger = logging.getLogger('account_deletion_logger')

# Logger für allgemeines Logging
app_logger = logging.getLogger('app_logger')

# Konfiguration der Logger für spezifische Logdateien
email_change_handler = logging.FileHandler(os.path.join(log_folder, 'email_change.txt'))
email_change_handler.setLevel(logging.INFO)
email_change_formatter = logging.Formatter('%(asctime)s - %(message)s')
email_change_handler.setFormatter(email_change_formatter)
email_change_logger.addHandler(email_change_handler)

password_change_handler = logging.FileHandler(os.path.join(log_folder, 'password_change.txt'))
password_change_handler.setLevel(logging.INFO)
password_change_formatter = logging.Formatter('%(asctime)s - %(message)s')
password_change_handler.setFormatter(password_change_formatter)
password_change_logger.addHandler(password_change_handler)

account_deletion_handler = logging.FileHandler(os.path.join(log_folder, 'account_deletion.txt'))
account_deletion_handler.setLevel(logging.INFO)
account_deletion_formatter = logging.Formatter('%(asctime)s - %(message)s')
account_deletion_handler.setFormatter(account_deletion_formatter)
account_deletion_logger.addHandler(account_deletion_handler)

# Konfiguration des allgemeinen Loggers für die App-Logs
app_handler = logging.FileHandler(os.path.join(log_folder, 'app_log.txt'))
app_handler.setLevel(logging.INFO)
app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)


# Passwortanforderungen überprüfen
def check_password_requirements(password):
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):  # Mindestens 1 Großbuchstabe
        return False
    if not re.search(r'[a-z]', password):  # Mindestens 1 Kleinbuchstabe
        return False
    if not re.search(r'\d', password):  # Mindestens 1 Zahl
        return False
    if not re.search(r'[\W_]', password):  # Mindestens 1 Sonderzeichen
        return False
    return True


@edit_profile.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    global user
    if request.method == 'POST':
        # E-Mail Änderung
        old_email = request.form.get('old_email')
        new_email = request.form.get('new_email')

        if new_email and new_email != current_user.email:
            user = User.query.filter_by(email=old_email).first()
            if user:
                # Überprüfen, ob die neue E-Mail bereits existiert
                if User.query.filter_by(email=new_email).first():
                    flash('Diese E-Mail-Adresse ist bereits vergeben.', 'danger')
                else:
                    # E-Mail ändern und loggen
                    old_email = current_user.email  # Vorherige E-Mail speichern
                    current_user.email = new_email
                    db.session.commit()

                    # Loggen der E-Mail-Änderung
                    email_change_logger.info(
                        f"User {current_user.id} changed their email from {old_email} to {new_email}.")

                    flash('E-Mail-Adresse wurde erfolgreich geändert!', 'success')
            else:
                flash('Die alte E-Mail-Adresse stimmt nicht mit deinem Konto überein.', 'danger')

        # Passwortänderung
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Sicherstellen, dass das Passwort den Anforderungen entspricht
        if new_password:
            if not check_password_requirements(new_password):
                flash(
                    'Das Passwort erfüllt nicht die Anforderungen. Es muss mindestens 12 Zeichen, einen Großbuchstaben, einen Kleinbuchstaben, eine Zahl und ein Sonderzeichen enthalten.',
                    'danger')
                return redirect(url_for('edit_profile.editprofile'))

            # Überprüfen, ob die Passwörter übereinstimmen
            if new_password != confirm_password:
                flash('Die Passwörter stimmen nicht überein.', 'danger')
                return redirect(url_for('edit_profile.editprofile'))

            # Passwort erfolgreich ändern
            hashed_password = generate_password_hash(new_password)  # Passwort sicher hashen
            current_user.password = hashed_password
            db.session.commit()

            # Logge die Passwortänderung
            password_change_logger.info(f"User {current_user.email} changed their password.")

            flash('Passwort wurde erfolgreich geändert!', 'success')

        # Konto löschen
        if 'delete_account' in request.form:
            try:
                # Logge den Account löschen Vorgang
                account_deletion_logger.info(f"User {current_user.email} deleted their account.")

                # Benutzer löschen
                db.session.delete(current_user)
                db.session.commit()

                flash('Dein Konto wurde erfolgreich gelöscht.', 'success')
                logout_user()  # Abmeldung des Benutzers nach der Löschung
                return redirect(url_for('home'))  # Zur Startseite umleiten

            except Exception as e:
                flash('Es gab ein Problem beim Löschen des Kontos. Bitte versuche es später erneut.', 'danger')
                app_logger.error(f"Error deleting account for user {current_user.email}: {e}")
                return redirect(url_for('edit_profile.editprofile'))

        # Nach erfolgreicher Änderung auf die Bearbeitungsseite zurückkehren
        return redirect(url_for('edit_profile.editprofile'))

    # Wenn der Request ein GET-Request ist, zeige das Edit-Profile-Template an
    return render_template('Dashboard/edit_profile.html', user_id=current_user.id)
