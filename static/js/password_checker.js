// Funktion zur Passwortstärkenprüfung
function checkPasswordStrength() {
    var password = document.getElementById("password").value;
    var strengthStatus = document.getElementById("strength-status");
    var strengthBar = document.getElementById("password-strength-bar");
    var requirements = document.getElementById("password-requirements").children;
    var commonPasswordMessage = document.getElementById("common-password-message");

    // Neue Regeln für Passwortanforderungen
    var lengthCheck = /^(?=.{12,})/;  // Passwort muss mindestens 12 Zeichen lang sein
    var uppercaseCheck = /[A-Z].*[A-Z].*[A-Z]/;  // Mindestens 3 Großbuchstaben
    var numberCheck = /\d.*\d/;  // Mindestens 2 Zahlen
    var specialCheck = /[!@#$%^&*(),.?":{}|<>].*[!@#$%^&*(),.?":{}|<>]/;  // Mindestens 2 Sonderzeichen
    var noRepeatCheck = /(.)\1{2,}/;  // Keine Wiederholungen wie 'aaa'

    // Überprüfen, ob alle Kriterien erfüllt sind
    var isValidLength = lengthCheck.test(password);
    var isValidUppercase = uppercaseCheck.test(password);
    var isValidNumber = numberCheck.test(password);
    var isValidSpecial = specialCheck.test(password);
    var isValidNoRepeat = !noRepeatCheck.test(password);

    // Anzeige der Anforderungen
    updateRequirement("length-check", isValidLength);
    updateRequirement("uppercase-check", isValidUppercase);
    updateRequirement("number-check", isValidNumber);
    updateRequirement("special-check", isValidSpecial);
    updateRequirement("no-repeat-check", isValidNoRepeat);

    // Bestimmen der Passwortstärke
    var validCount = [isValidLength, isValidUppercase, isValidNumber, isValidSpecial, isValidNoRepeat].filter(Boolean).length;

    // Setze die Stärke
    if (validCount === 5) {
        strengthStatus.innerHTML = "Sehr stark";
        strengthStatus.style.color = "green";
        strengthBar.style.width = "100%";
        strengthBar.style.backgroundColor = "green";
    } else if (validCount >= 4) {
        strengthStatus.innerHTML = "Stark";
        strengthStatus.style.color = "yellow";
        strengthBar.style.width = "80%";
        strengthBar.style.backgroundColor = "yellow";
    } else if (validCount >= 3) {
        strengthStatus.innerHTML = "Mittel";
        strengthStatus.style.color = "orange";
        strengthBar.style.width = "60%";
        strengthBar.style.backgroundColor = "orange";
    } else {
        strengthStatus.innerHTML = "Schwach";
        strengthStatus.style.color = "red";
        strengthBar.style.width = "40%";
        strengthBar.style.backgroundColor = "red";
    }

    // Überprüfe, ob das Passwort zu gängig ist
    checkIfCommonPassword(password, commonPasswordMessage);
}

// Hilfsfunktion zur Aktualisierung der Anforderungsanzeige
function updateRequirement(id, isValid) {
    var element = document.getElementById(id);
    if (isValid) {
        element.classList.add("valid");
        element.classList.remove("invalid");
    } else {
        element.classList.add("invalid");
        element.classList.remove("valid");
    }
}

// Überprüfe, ob das Passwort ein gängiges Passwort ist
function checkIfCommonPassword(password, commonPasswordMessage) {
    // Verwende vollständige URL für den Fetch-Aufruf
    fetch('/password_checker', {  // Endpunkt korrigiert zu '/password_checker'
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            commonPasswordMessage.innerHTML = data.message;
            commonPasswordMessage.style.color = "red";
        } else {
            commonPasswordMessage.innerHTML = "";
        }
    })
    .catch(error => {
        console.error('Fehler beim Überprüfen des Passworts:', error);
        commonPasswordMessage.innerHTML = "Fehler bei der Anfrage!";
        commonPasswordMessage.style.color = "red";
    });
}

// Passwort-Übereinstimmung prüfen
function checkPasswordMatch() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password").value;
    var matchMessage = document.getElementById("password-match-message");

    if (password !== confirmPassword) {
        matchMessage.innerHTML = "Passwörter stimmen nicht überein!";
        matchMessage.style.color = "red";
    } else {
        matchMessage.innerHTML = "Passwörter stimmen überein!";
        matchMessage.style.color = "green";
    }
}