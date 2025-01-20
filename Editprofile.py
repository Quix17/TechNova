import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from models import db, User

# Blueprint erstellen
edit_profile = Blueprint('edit_profile', __name__)

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
                    user.email = new_email
                    db.session.commit()
                    flash('E-Mail-Adresse wurde erfolgreich geändert!', 'success')
            else:
                flash('Die alte E-Mail-Adresse stimmt nicht mit deinem Konto überein.', 'danger')

        # Passwort ändern
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Sicherstellen, dass das Passwort nicht None ist und den Anforderungen entspricht
        if new_password:
            if not check_password_requirements(new_password):
                flash('Das Passwort erfüllt nicht die Anforderungen. Es muss mindestens 12 Zeichen, einen Großbuchstaben, einen Kleinbuchstaben, eine Zahl und ein Sonderzeichen enthalten.', 'danger')
                return redirect(url_for('edit_profile.editprofile'))

            # Überprüfen, ob die Passwörter übereinstimmen
            if new_password != confirm_password:
                flash('Die Passwörter stimmen nicht überein.', 'danger')
                return redirect(url_for('edit_profile.editprofile'))

            # Passwort erfolgreich ändern
            hashed_password = generate_password_hash(new_password)  # Passwort sicher hashen
            current_user.password = hashed_password
            db.session.commit()
            flash('Passwort wurde erfolgreich geändert!', 'success')

        # Konto löschen
        if 'delete_account' in request.form:
            try:
                print(f"Benutzer zum Löschen: {current_user}")
                # Benutzer löschen
                db.session.delete(current_user)
                db.session.commit()

                # Benutzer abmelden und Weiterleitung
                logout_user()
                flash('Dein Konto wurde erfolgreich gelöscht.', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash(f'Es gab ein Problem beim Löschen deines Kontos: {str(e)}. Bitte versuche es später erneut.', 'danger')

    return render_template('Dashboard/edit_profile.html')