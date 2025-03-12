document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("info-modal");
    const modalOkButton = document.getElementById("modal-ok");

    // Debug: Was speichert localStorage?
    console.log("LocalStorage Value:", localStorage.getItem("modalAccepted"));

    // Korrekte Prüfung, ob es "true" ist
    if (localStorage.getItem("modalAccepted") === "true") {
        modal.style.display = "none";
    } else {
        modal.style.display = "flex";
    }

    // Button-Click -> Speichern & ausblenden
    modalOkButton.addEventListener("click", function () {
        localStorage.setItem("modalAccepted", "true");
        console.log("LocalStorage gespeichert als 'true'");
        modal.style.opacity = "0";
        setTimeout(() => {
            modal.style.display = "none";
        }, 300);
    });
});
