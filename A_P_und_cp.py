import re
import random
import string
from flask import Flask

app = Flask(__name__)

# Passwortanforderungen
def check_password_requirements(password):
    # Mindestens 26 Zeichen
    length_check = len(password) >= 12
    # Mindestens 5 Großbuchstaben
    uppercase_check = len(re.findall(r'[A-Z]', password)) >= 3
    # Mindestens 2 Zahlen
    number_check = len(re.findall(r'\d', password)) >= 2
    # Mindestens 2 Sonderzeichen
    special_check = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password)) >= 2

    # Rückgabe der Ergebnisse der Passwortanforderungen
    return length_check, uppercase_check, number_check, special_check

# Funktion zum Generieren eines Passworts mit einer bestimmten Länge
def password_generator(length):
    if length < 12 or length > 64:
        return None
    # Erzeuge ein zufälliges Passwort mit Großbuchstaben, Kleinbuchstaben, Zahlen und Sonderzeichen
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for i in range(length))
    return password

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