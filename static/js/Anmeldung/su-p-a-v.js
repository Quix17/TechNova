// Funktion zum Umschalten des Passworts für das erste Passwortfeld
function togglePassword() {
    const passwordField = document.getElementById('password');
    const toggleIcon = document.getElementById('toggle-password').querySelector('i');

    if (passwordField.type === 'password') {
        passwordField.type = 'text'; // Passwort sichtbar machen
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash'); // Auge-Symbol ändern
    } else {
        passwordField.type = 'password'; // Passwort wieder verbergen
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye'); // Auge-Symbol zurücksetzen
    }
}

// Funktion zum Umschalten des Passworts für das Bestätigungs-Passwortfeld
function toggleConfirmPassword() {
    const confirmPasswordField = document.getElementById('confirm-password');
    const toggleIcon = document.getElementById('toggle-confirm-password').querySelector('i');

    if (confirmPasswordField.type === 'password') {
        confirmPasswordField.type = 'text'; // Passwort sichtbar machen
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash'); // Auge-Symbol ändern
    } else {
        confirmPasswordField.type = 'password'; // Passwort wieder verbergen
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye'); // Auge-Symbol zurücksetzen
    }
}