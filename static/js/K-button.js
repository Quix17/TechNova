// Funktion für das Öffnen der Profilbearbeitungs-Seite
document.getElementById("settings").addEventListener("click", function() {
    window.location.href = "/edit_profile"; // Weiterleitung zur Profilbearbeitungs-Seite
});

// Funktion für das Logout
document.getElementById("logout").addEventListener("click", function() {
    window.location.href = "/logout"; // Weiterleitung zur Logout-Route
});
