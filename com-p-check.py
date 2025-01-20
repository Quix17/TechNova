from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Lade die Liste häufiger Passwörter
def load_common_passwords(file_path):
    try:
        with open(file_path, 'r') as f:
            common_passwords = set(line.strip().lower() for line in f)
        return common_passwords
    except FileNotFoundError:
        print("Die Datei mit den häufigen Passwörtern wurde nicht gefunden.")
        return set()

# Der Pfad zu der Datei mit den häufigen Passwörtern
common_password_file = '/static/txt/common_passwords.txt'
common_passwords = load_common_passwords(common_password_file)

@app.route('/')
def index():
    return render_template('Anmeldung/signup.html')

@app.route('/password_checker', methods=['POST'])
def check_password():
    # Sicherstellen, dass die Anfrage JSON enthält
    try:
        data = request.get_json()
        password = data.get('password')
    except Exception as e:
        return jsonify({"message": "Ungültige Anfrage, JSON erwartet!"}), 400

    if not password:
        return jsonify({"message": "Passwort darf nicht leer sein!"}), 400

    # Überprüfe, ob das Passwort in der Liste häufiger Passwörter ist
    if password.lower() in common_passwords:
        return jsonify({"message": "Das Passwort ist zu gängig und sollte vermieden werden!"}), 400

    # Wenn das Passwort sicher ist
    return jsonify({"message": "Das Passwort ist sicher."}), 200

if __name__ == '__main__':
    app.run(debug=True)