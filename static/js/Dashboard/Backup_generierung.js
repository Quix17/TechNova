function showMessage(message, type) {
    let msgBox = document.getElementById("msg-box");

    if (!msgBox) {
        console.error("❌ Fehler: #msg-box wurde nicht gefunden!");
        return;
    }

    console.log("🟢 showMessage() wurde aufgerufen:", message, type);

    // Vorherige Klassen und Stile entfernen
    msgBox.classList.remove("hide", "hidden", "msg-success", "msg-fail");
    msgBox.style.display = "block"; // Falls `hidden` noch aktiv war

    // Neue Nachricht setzen und anzeigen
    msgBox.textContent = message;
    msgBox.classList.add(type, "show");

    // Nachricht nach 3 Sekunden ausblenden
    setTimeout(() => {
        console.log("🔴 Verstecke Nachricht jetzt...");
        msgBox.classList.remove("show");
        msgBox.classList.add("hide");

        setTimeout(() => {
            msgBox.classList.add("hidden");
            msgBox.style.display = "none";
            console.log("📌 Aktuelle Klassen nach Verstecken:", msgBox.classList);
        }, 500);
    }, 3000);
}
