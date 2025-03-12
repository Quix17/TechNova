document.addEventListener("DOMContentLoaded", function() {
    // Anime.js Parameter
    const BLINK_SPEED = 0.075;
    const TOGGLE_SPEED = 0.125;
    const ENCRYPT_SPEED = 0.3; // Schnellere Animation für bessere Reaktionsfähigkeit

    let busy = false;

    const TOGGLE_PASSWORD = document.getElementById("toggle-password");
    const TOGGLE_CONFIRM_PASSWORD = document.getElementById("toggle-confirm-password");

    const INPUT_PASSWORD = document.getElementById("password");
    const INPUT_CONFIRM_PASSWORD = document.getElementById("confirm-password");

    const PROXY_PASSWORD = document.createElement('div');
    const PROXY_CONFIRM_PASSWORD = document.createElement('div');

    PROXY_PASSWORD.style.position = "absolute";
    PROXY_PASSWORD.style.visibility = "hidden";
    PROXY_CONFIRM_PASSWORD.style.position = "absolute";
    PROXY_CONFIRM_PASSWORD.style.visibility = "hidden";

    document.body.appendChild(PROXY_PASSWORD);
    document.body.appendChild(PROXY_CONFIRM_PASSWORD);

    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~,.<>?/;":][}{+_)(*&^%$#@!±=-§';

    // Verbesserte Scramble-Funktion mit Anime.js
    function scrambleText(element, originalText, targetText, duration, callback) {
        // Erstelle ein Proxy-Objekt für die Animation
        const proxy = { value: 0 };

        // Anime.js für die flüssige Animation
        anime({
            targets: proxy,
            value: 1,
            duration: duration * 1000, // Dauer der Animation in ms
            easing: "easeInOutQuad",
            update: function(anim) {
                const progress = proxy.value;
                const revealedLength = Math.floor(progress * targetText.length);

                // Generiere für jeden Frame neue zufällige Zeichen für nicht enthüllte Zeichen
                let result = "";
                for (let i = 0; i < targetText.length; i++) {
                    if (i < revealedLength) {
                        result += targetText[i];
                    } else {
                        result += chars[Math.floor(Math.random() * chars.length)];
                    }
                }

                element.value = result;
            },
            complete: function() {
                element.value = targetText;
                if (callback) callback();
            }
        });
    }

    // WICHTIG: Definiere die Toggle-Funktionen global, damit sie von HTML onclick aufgerufen werden können
    window.togglePassword = function() {
        togglePasswordFunction(INPUT_PASSWORD, TOGGLE_PASSWORD, PROXY_PASSWORD);
    };

    window.toggleConfirmPassword = function() {
        togglePasswordFunction(INPUT_CONFIRM_PASSWORD, TOGGLE_CONFIRM_PASSWORD, PROXY_CONFIRM_PASSWORD);
    };

    // Die eigentliche Toggle-Funktion (jetzt mit anderem Namen zur Vermeidung von Konflikten)
    const togglePasswordFunction = (input, toggle, proxy) => {
        if (busy) return;
        busy = true;

        const isPassword = input.type === "password";
        const val = input.value;
        toggle.setAttribute('aria-pressed', isPassword);
        const eyeIcon = toggle.querySelector('i');

        if (isPassword) {
            // Wechseln zu Text-Modus (Passwort anzeigen)
            eyeIcon.classList.remove("fa-eye");
            eyeIcon.classList.add("fa-eye-slash");

            // Erstelle ein temporäres Input-Element für den Text
            const tempInput = document.createElement('input');
            tempInput.type = 'text';
            tempInput.value = val;
            tempInput.style.position = 'absolute';
            tempInput.style.opacity = '0';
            document.body.appendChild(tempInput);

            // Ändere zuerst den Typ und dann animiere
            input.type = "text";

            // Animation für das Anzeigen des Passworts mit Anime.js
            const maskedText = new Array(val.length).fill("•").join("");
            scrambleText(
                input,
                maskedText,
                val,
                ENCRYPT_SPEED,
                () => {
                    input.value = val; // Das ursprüngliche Passwort wiederherstellen
                    document.body.removeChild(tempInput);
                    busy = false;
                }
            );
        } else {
            // Wechseln zu Password-Modus (Passwort verstecken)
            eyeIcon.classList.remove("fa-eye-slash");
            eyeIcon.classList.add("fa-eye");

            // Animation für das Verstecken des Passworts mit Anime.js
            const maskedText = new Array(val.length).fill("•").join("");
            scrambleText(
                input,
                val,
                maskedText,
                ENCRYPT_SPEED,
                () => {
                    input.type = "password";
                    input.value = val; // Das ursprüngliche Passwort wiederherstellen
                    busy = false;
                }
            );
        }
    };

    // Event-Listener für das Toggle der Passwörter (als Alternative zum onclick im HTML)
    TOGGLE_PASSWORD.addEventListener('click', window.togglePassword);
    TOGGLE_CONFIRM_PASSWORD.addEventListener('click', window.toggleConfirmPassword);

    // Füge Tastatur-Unterstützung hinzu
    TOGGLE_PASSWORD.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            window.togglePassword();
        }
    });

    TOGGLE_CONFIRM_PASSWORD.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            window.toggleConfirmPassword();
        }
    });

    // CSS für bessere visuelle Rückmeldung ohne blauen Rand
    const style = document.createElement('style');
    style.textContent = `
        #password, #confirm-password {
            transition: border-color 0.3s ease;
            outline: none; /* Entfernt den Standard-Fokus-Rand */
        }
        #password:focus, #confirm-password:focus {
            outline: none; /* Entfernt den Standard-Fokus-Rand */
            box-shadow: none; /* Entfernt jeden möglichen Schatten */
            border-color: inherit; /* Behält die ursprüngliche Rahmenfarbe bei */
        }
        #toggle-password, #toggle-confirm-password {
            cursor: pointer;
            transition: opacity 0.3s ease;
        }
        #toggle-password:hover, #toggle-confirm-password:hover {
            opacity: 0.8;
        }
        #toggle-password:active, #toggle-confirm-password:active {
            opacity: 0.6;
        }
    `;
    document.head.appendChild(style);

    // Verhindern des Formularabsendens
    const FORM = document.querySelector('form');
    if (FORM) {
        FORM.addEventListener('submit', (e) => {
            e.preventDefault();
            // Hier kannst du deine eigene Formularvalidierung hinzufügen
        });
    }
});