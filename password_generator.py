import random
import string

# Funktion zum Generieren eines sicheren Passworts mit einer bestimmten Länge
def generate_password(length):
    while True:
        password = []

        # 5 Großbuchstaben
        password.extend(random.choices(string.ascii_uppercase, k=5))

        # 2 Zahlen
        password.extend(random.choices(string.digits, k=2))

        # 2 Sonderzeichen
        password.extend(random.choices(string.punctuation, k=2))

        # Füllzeichen, um die Passwortlänge zu erreichen
        password.extend(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length - len(password)))

        # Passwort mixen
        random.shuffle(password)

        # Umwandlung in String
        password = ''.join(password)

        # Prüfen, ob das Passwort die Anforderungen erfüllt
        if (len(password) >= 12 and
            sum(1 for c in password if c.isupper()) >= 3 and
            sum(1 for c in password if c.isdigit()) >= 2 and
            sum(1 for c in password if c in string.punctuation) >= 2 and
            not has_repeated_characters(password)):
            return password

# Funktion zur Überprüfung von Zeichenwiederholungen
def has_repeated_characters(password):
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            return True
    return False