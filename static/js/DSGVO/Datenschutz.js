// Datenschutz-Seite spezifische JS (z.B. für Cookie-Banner oder interaktive Elemente)
document.addEventListener("DOMContentLoaded", function() {
    // Beispiel: Ein einfacher Cookie-Banner
    const cookieBanner = document.createElement("div");
    cookieBanner.id = "cookie-banner";
    cookieBanner.innerHTML = `
        <p>Wir verwenden Cookies, um die Benutzererfahrung zu verbessern. Durch die Nutzung unserer Website stimmst du der Verwendung von Cookies zu. <a href="/cookies">Mehr erfahren</a></p>
        <button id="accept-cookies">Akzeptieren</button>
    `;
    document.body.appendChild(cookieBanner);

    document.getElementById("accept-cookies").addEventListener("click", function() {
        cookieBanner.style.display = "none";
        localStorage.setItem("cookiesAccepted", "true");
    });

    if (localStorage.getItem("cookiesAccepted")) {
        cookieBanner.style.display = "none";
    }
});