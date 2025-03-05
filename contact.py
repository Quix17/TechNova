from flask import Blueprint, request, flash, redirect, url_for, session
from flask_login import current_user
import os
from datetime import datetime

# Blueprint erstellen
contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/submit_contact_form', methods=['POST'])
def submit_contact_form_handler():
    # Import der Logger innerhalb der Funktion
    from app import user_action_logger, user_error_logger

    # Formulardaten empfangen
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Benutzerbezogene Daten
    user_ip = request.remote_addr
    user_id = current_user.id if current_user.is_authenticated else 'Anonym'
    username = current_user.email if current_user.is_authenticated else 'Unbekannt'
    user_agent = request.headers.get('User-Agent', 'Unbekannt')
    referer = request.headers.get('Referer', 'Unbekannt')
    session_data = session.sid if hasattr(session, 'sid') else 'Keine Session'

    # Aktuelles Datum und Uhrzeit
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Verzeichnis für gespeicherte Formulardaten
    form_folder = 'form_data'
    if not os.path.exists(form_folder):
        try:
            os.makedirs(form_folder)
        except Exception as e:
            flash(f"Fehler beim Erstellen des Ordners: {e}", 'danger')
            return redirect(url_for('contact.contact_form'))

    # Detaillierte Logging-Nachricht
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
        return redirect(url_for('contact.contact_form'))

    # Erfolgsnachricht
    flash("Vielen Dank für Ihre Nachricht. Wir werden uns in Kürze bei Ihnen melden, per E-Mail.", 'success')
    return redirect(url_for('contact.contact_form'))