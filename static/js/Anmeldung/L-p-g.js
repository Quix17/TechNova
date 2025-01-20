// Funktion zum Abrufen eines generierten Passworts mit der gewünschten Länge vom Flask-Endpunkt
async function generateRandomPassword() {
    const passwordLength = document.getElementById('password-length').value;  // Holen der Länge des Passworts vom Slider

    try {
        // Anfrage an Flask-Server mit der Länge als Parameter
        const response = await fetch(`/password_generator/${passwordLength}`);
        if (response.ok) {
            const data = await response.json();  // Antwort als JSON
            const generatedPassword = data.password;  // Passwort aus der Antwort
            document.getElementById('generated-password').value = generatedPassword;  // Passwort in das Feld einfügen
        } else {
            alert("Fehler beim Abrufen des Passworts.");
        }
    } catch (error) {
        alert("Fehler beim Abrufen des Passworts.");
        console.error(error);
    }
}

// Funktion zum Aktualisieren der Anzeige der Passwortlänge (live)
function updatePasswordLength() {
    const length = document.getElementById('password-length').value;
    // Anzeige der aktuellen Passwortlänge unter dem Slider
    document.getElementById('password-length-display').textContent = length;
    // Passwort neu generieren, wenn der Slider bewegt wird
    generateRandomPassword();
}

// Initiales Passwort generieren
generateRandomPassword();