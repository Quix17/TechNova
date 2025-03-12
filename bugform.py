import os
from flask import request

# Sicherstellen, dass der Speicherordner existiert
DATA_FOLDER = "form_data"
os.makedirs(DATA_FOLDER, exist_ok=True)

def save_bug_report():
    """Speichert die Bug-Report-Daten in einer Datei."""
    data = request.form

    title = data.get("title", "Kein Titel")
    severity = data.get("severity", "Nicht angegeben")
    module = data.get("module", "Nicht angegeben")
    browser = data.get("browser", "Nicht angegeben")
    os_info = data.get("os", "Nicht angegeben")
    description = data.get("description", "Keine Beschreibung")
    screenshot = data.get("screenshot", "Kein Link")
    name = data.get("name", "Anonym")
    email = data.get("email", "Keine E-Mail")

    file_path = os.path.join(DATA_FOLDER, "bug_reports.txt")

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"=== Neuer Bug-Report ===\n")
        file.write(f"Titel: {title}\n")
        file.write(f"Schweregrad: {severity}\n")
        file.write(f"Modul: {module}\n")
        file.write(f"Browser: {browser}\n")
        file.write(f"Betriebssystem: {os_info}\n")
        file.write(f"Beschreibung: {description}\n")
        file.write(f"Screenshot: {screenshot}\n")
        file.write(f"Name: {name}\n")
        file.write(f"E-Mail: {email}\n")
        file.write(f"========================\n\n")

    return "Bug-Report erfolgreich gespeichert!"
