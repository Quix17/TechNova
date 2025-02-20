// Funktion zur Passwortvalidierung
function checkPassword() {
    var password = document.getElementById('new_password').value;
    var confirmPassword = document.getElementById('confirm_password').value;

    var length = document.getElementById('length');
    var uppercase = document.getElementById('uppercase');
    var lowercase = document.getElementById('lowercase');
    var number = document.getElementById('number');
    var special = document.getElementById('special');

    // Länge prüfen
    if (password.length >= 12) {
        length.classList.add('valid');
        length.classList.remove('invalid');
    } else {
        length.classList.add('invalid');
        length.classList.remove('valid');
    }

    // Großbuchstabe prüfen
    if (/[A-Z]/.test(password)) {
        uppercase.classList.add('valid');
        uppercase.classList.remove('invalid');
    } else {
        uppercase.classList.add('invalid');
        uppercase.classList.remove('valid');
    }

    // Kleinbuchstabe prüfen
    if (/[a-z]/.test(password)) {
        lowercase.classList.add('valid');
        lowercase.classList.remove('invalid');
    } else {
        lowercase.classList.add('invalid');
        lowercase.classList.remove('valid');
    }

    // Zahl prüfen
    if (/\d/.test(password)) {
        number.classList.add('valid');
        number.classList.remove('invalid');
    } else {
        number.classList.add('invalid');
        number.classList.remove('valid');
    }

    // Sonderzeichen prüfen
    if (/[\W_]/.test(password)) {
        special.classList.add('valid');
        special.classList.remove('invalid');
    } else {
        special.classList.add('invalid');
        special.classList.remove('valid');
    }

    // Bestätigungs-Passwort validieren
    if (password === confirmPassword) {
        document.getElementById('confirm_password').style.borderColor = "green";
    } else {
        document.getElementById('confirm_password').style.borderColor = "red";
    }
}

// Funktion zur Generierung von Backup-Codes
function generateBackupCodes() {
    var userId = document.getElementById("user-id").value;
    var now = Date.now();

    // Hole die verbleibende Timeout-Zeit vom Server
    fetch('/get_remaining_timeout', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        var remainingTimeout = data.remaining_timeout; // Zeit in Stunden
        
        // Wenn es einen verbleibenden Timeout gibt, zeige die Warnung
        if (remainingTimeout > 0) {
            alert("Du kannst erst in " + Math.ceil(remainingTimeout) + " Stunden erneut Backup-Codes generieren.");
            return;
        }

        // Erstelle die Backup-Codes
        var codes = {};
        for (var i = 0; i < 5; i++) {
            var code = Math.random().toString(36).substring(2, 8).toUpperCase();
            codes[code] = { used: false };
        }

        // Zeige die generierten Codes an
        document.getElementById("backup-codes").innerHTML = "<h3>Backup-Codes:</h3><ul>" +
            Object.keys(codes).map(code => `<li>${code}</li>`).join('') + "</ul>";

        // Sende die Backup-Codes und die Benutzer-ID an den Server
        fetch('/save_backup_codes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId, codes: codes })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Aktualisiere die Generierungsanzahl und den Timeout auf dem Server
                fetch('/update_backup_code_info', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Backup-Codes wurden erfolgreich gespeichert.");
                    } else {
                        console.error("Fehler beim Aktualisieren der Generierungsanzahl.");
                        alert("Fehler beim Speichern der Backup-Codes.");
                    }
                });
            } else {
                console.error("Fehler beim Speichern der Backup-Codes:", data.message);
                alert("Fehler beim Speichern der Backup-Codes.");
            }
        })
        .catch(error => {
            console.error("Fehler:", error);
            alert("Es gab einen Fehler bei der Anfrage.");
        });
    });
}


// Funktion zur Steuerung der Tabs (Automatische Aktivierung des ersten Tabs)
document.addEventListener('DOMContentLoaded', function () {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Entferne 'active' Klasse von allen Tabs und Pane-Inhalten
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Füge 'active' Klasse hinzu für den angeklickten Tab und den zugehörigen Pane
            this.classList.add('active');
            const activeTab = this.id.replace('tab-', '');
            document.getElementById(activeTab).classList.add('active');
        });
    });

    // Standardmäßig den "Persönliche Infos"-Tab aktivieren
    document.getElementById('tab-info').click();
});