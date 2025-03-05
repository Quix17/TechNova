function showError(message) {
    console.log("Fehlermeldung wird angezeigt:", message);
    const errorMessage = document.getElementById('error-message');

    if (!errorMessage) {
        console.error("❌ Fehler: Element mit ID 'error-message' nicht gefunden!");
        return;
    }

    errorMessage.textContent = message;

    // Zeige die Nachricht smooth an
    errorMessage.classList.remove('hide');
    errorMessage.classList.add('show');

    // Nach 4 Sekunden langsam ausblenden
    setTimeout(() => {
        errorMessage.classList.remove('show');
        errorMessage.classList.add('hide');
    }, 4000);
}


async function login() {
    const email = document.getElementById('email').value;
    const backupCode = document.getElementById('backup-code').value;

    try {
        const response = await fetch('/login_with_backup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, backup_code: backupCode })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || "Ein unbekannter Fehler ist aufgetreten.");
        }

        // Falls Erfolg
        if (result.status === "success") {
            window.location.href = `/dashboard_id${result.user_id}`;
        } else {
            showError(result.message);
        }

    } catch (error) {
        console.error("❌ Fehler: ", error.message);
        showError(error.message);
    }
}