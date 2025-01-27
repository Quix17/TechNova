// Funktion zur Passwortstärkenprüfung
function checkPasswordStrength() {
    const password = document.getElementById("password").value;
    const strengthStatus = document.getElementById("strength-status");
    const strengthBar = document.getElementById("password-strength-bar");
    const requirements = document.getElementById("password-requirements").children;
    const commonPasswordMessage = document.getElementById("common-password-message");

    // Neue Regeln für Passwortanforderungen
    const lengthCheck = /^(?=.{12,})/;  // Passwort muss mindestens 12 Zeichen lang sein
    const uppercaseCheck = /[A-Z].*[A-Z].*[A-Z]/;  // Mindestens 3 Großbuchstaben
    const numberCheck = /\d.*\d/;  // Mindestens 2 Zahlen
    const specialCheck = /[!@#$%^&*(),.?":{}|<>].*[!@#$%^&*(),.?":{}|<>]/;  // Mindestens 2 Sonderzeichen
    const noRepeatCheck = /(.)\1{2,}/;  // Keine Wiederholungen wie 'aaa'

    // Überprüfen, ob alle Kriterien erfüllt sind
    const isValidLength = lengthCheck.test(password);
    const isValidUppercase = uppercaseCheck.test(password);
    const isValidNumber = numberCheck.test(password);
    const isValidSpecial = specialCheck.test(password);
    const isValidNoRepeat = !noRepeatCheck.test(password);

    // Anzeige der Anforderungen
    updateRequirement("length-check", isValidLength);
    updateRequirement("uppercase-check", isValidUppercase);
    updateRequirement("number-check", isValidNumber);
    updateRequirement("special-check", isValidSpecial);
    updateRequirement("no-repeat-check", isValidNoRepeat);

    // Bestimmen der Passwortstärke
    const validCount = [isValidLength, isValidUppercase, isValidNumber, isValidSpecial, isValidNoRepeat].filter(Boolean).length;

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
    const element = document.getElementById(id);
    if (isValid) {
        element.classList.add("valid");
        element.classList.remove("invalid");
    } else {
        element.classList.add("invalid");
        element.classList.remove("valid");
    }
}

// Überprüfe, ob das Passwort zu gängig ist
function checkIfCommonPassword(password, commonPasswordMessage) {
    fetch('/password_checker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_common) {
            commonPasswordMessage.innerHTML = "Das Passwort ist zu gängig und sollte vermieden werden!";
            commonPasswordMessage.style.color = "red";
        } else {
            commonPasswordMessage.innerHTML = "Das Passwort ist sicher.";
            commonPasswordMessage.style.color = "green";
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
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const matchMessage = document.getElementById("password-match-message");

    if (password !== confirmPassword) {
        matchMessage.innerHTML = "Passwörter stimmen nicht überein!";
        matchMessage.style.color = "red";
    } else {
        matchMessage.innerHTML = "Passwörter stimmen überein!";
        matchMessage.style.color = "green";
    }
}

async function checkIfCommonPassword(password) {
    const commonPasswordMessage = document.getElementById("common-password-message");

    if (!commonPasswordMessage) {
        console.error("Element mit der ID 'common-password-message' nicht gefunden.");
        return;
    }

    try {
        console.log("Sende Passwort zur Überprüfung:", password);  // Debugging: Ausgabe des Passworts

        const response = await fetch('/password_checker', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password: password })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        console.log(data);  // Debugging: Antwort von der API ausgeben

        // Überprüfe die Antwort, um zu sehen, ob das Passwort gängig ist
        if (data.is_common) {
            commonPasswordMessage.innerHTML = "Das Passwort ist zu gängig und sollte vermieden werden!";
            commonPasswordMessage.style.color = "red";
        } else {
            commonPasswordMessage.innerHTML = "Das Passwort ist sicher.";
            commonPasswordMessage.style.color = "green";
        }
    } catch (error) {
        console.error("Fehler beim Überprüfen des Passworts:", error);
        commonPasswordMessage.innerHTML = "Fehler bei der Anfrage!";
        commonPasswordMessage.style.color = "red";
    }
}