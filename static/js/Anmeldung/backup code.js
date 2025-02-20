function showError(message) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorMessage.classList.add('show');

    // Fehlernachricht nach 4 Sekunden ausblenden
    setTimeout(() => {
        errorMessage.classList.remove('show');
    }, 4000);
}

async function login() {
    const email = document.getElementById('email').value;
    const backupCode = document.getElementById('backup-code').value;

    const response = await fetch('/login_with_backup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, backup_code: backupCode })
    });

    const result = await response.json();

    if (result.status === 'error') {
        showError(result.message);
    } else {
        window.location.href = "/dashboard"; // Weiterleitung nach erfolgreichem Login
    }
}
