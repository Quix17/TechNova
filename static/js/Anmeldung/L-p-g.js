document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("password-length");
    const lengthDisplay = document.getElementById("password-length-display");
    const passwordField = document.getElementById("generated-password");

    // Funktion zum Abrufen eines generierten Passworts mit der gewünschten Länge vom Flask-Endpunkt
    async function generateRandomPassword() {
        const passwordLength = slider.value;

        try {
            const response = await fetch(`/password_generator/${passwordLength}`);
            if (response.ok) {
                const data = await response.json();
                passwordField.value = data.password;
            } else {
                console.error("Fehler beim Abrufen des Passworts.");
            }
        } catch (error) {
            console.error("Fehler beim Abrufen des Passworts.", error);
        }
    }

    function updatePasswordLengthAndGenerate() {
        lengthDisplay.textContent = slider.value;
        generateRandomPassword(); // Generiere ein neues Passwort bei jeder Änderung
    }

    // Event-Listener: Bei jeder Bewegung des Sliders aktualisieren
    slider.addEventListener("input", updatePasswordLengthAndGenerate);

    // Erstes Passwort generieren
    generateRandomPassword();
});
