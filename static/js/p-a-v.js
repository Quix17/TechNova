document.addEventListener("DOMContentLoaded", function() {
    const togglePassword = document.getElementById("toggle-password");
    const passwordField = document.getElementById("password");

    togglePassword.addEventListener("click", function() {
        // Toggle Passwortanzeige
        const type = passwordField.type === "password" ? "text" : "password";
        passwordField.type = type;

        // Icon wechseln zwischen 'fa-eye' (sichtbar) und 'fa-eye-slash' (unsichtbar)
        togglePassword.innerHTML = passwordField.type === "password" ?
            `<i class="fas fa-eye"></i>` :
            `<i class="fas fa-eye-slash"></i>`;
    });
});