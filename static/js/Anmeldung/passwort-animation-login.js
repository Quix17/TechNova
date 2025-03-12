document.addEventListener("DOMContentLoaded", function () {
    const TOGGLE_SPEED = 0.125; // Geschwindigkeit der Animation
    const ENCRYPT_SPEED = 0.3; // Schnellere Animation für bessere Reaktionsfähigkeit

    let busy = false;

    const TOGGLE = document.getElementById("toggle-password");
    const INPUT = document.getElementById("password");
    const PROXY = document.createElement("div");
    PROXY.style.position = "absolute";
    PROXY.style.visibility = "hidden";

    const chars =
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~,.<>?/;\":][}{+_)(*&^%$#@!±=-§";

    // Funktion zum Scramblen des Texts mit verbesserter Animation
    function scrambleText(element, originalText, targetText, duration, callback) {
        const startTime = Date.now();
        const endTime = startTime + (duration * 1000);

        // Erstelle eine Kopie des Originalwerts für die Animation
        let scrambledText = originalText.split("").map(() =>
            chars[Math.floor(Math.random() * chars.length)]
        ).join("");

        function update() {
            const now = Date.now();
            const progress = Math.min(1, (now - startTime) / (duration * 1000));

            if (progress < 1) {
                // Generiere für jeden Frame neue zufällige Zeichen für nicht enthüllte Zeichen
                const revealedLength = Math.floor(progress * targetText.length);
                const currentScrambled = targetText.split("").map((char, i) => {
                    if (i < revealedLength) {
                        return targetText[i];
                    } else {
                        return chars[Math.floor(Math.random() * chars.length)];
                    }
                }).join("");

                element.value = currentScrambled;
                requestAnimationFrame(update);
            } else {
                // Animation abgeschlossen
                element.value = targetText;
                if (callback) callback();
            }
        }

        // Starte die Animation mit requestAnimationFrame für bessere Performance
        requestAnimationFrame(update);
    }

    // Event für das Anzeigen/Verstecken des Passworts
    TOGGLE.addEventListener("click", () => {
        if (busy) return;
        busy = true;

        const isPassword = INPUT.type === "password";
        const val = INPUT.value;
        TOGGLE.setAttribute("aria-pressed", isPassword);
        const eyeIcon = document.getElementById("eye-icon");

        if (isPassword) {
            // Wechseln zu Text-Modus (Passwort anzeigen)
            const tempInput = document.createElement('input');
            tempInput.type = 'text';
            tempInput.value = val;
            tempInput.style.position = 'absolute';
            tempInput.style.opacity = '0';
            document.body.appendChild(tempInput);

            eyeIcon.classList.remove("fa-eye");
            eyeIcon.classList.add("fa-eye-slash");

            // Zuerst Typ ändern, dann animieren
            INPUT.type = "text";

            // Animation für das Anzeigen des Passworts
            scrambleText(INPUT, new Array(val.length).fill("•").join(""), val, ENCRYPT_SPEED, () => {
                busy = false;
                document.body.removeChild(tempInput);
            });
        } else {
            // Wechseln zu Password-Modus (Passwort verstecken)
            eyeIcon.classList.remove("fa-eye-slash");
            eyeIcon.classList.add("fa-eye");

            // Animation für das Verstecken des Passworts
            scrambleText(INPUT, val, new Array(val.length).fill("•").join(""), ENCRYPT_SPEED, () => {
                INPUT.type = "password";
                INPUT.value = val; // Das ursprüngliche Passwort wiederherstellen
                busy = false;
            });
        }
    });

    // Füge Tastatur-Unterstützung hinzu
    TOGGLE.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            TOGGLE.click();
        }
    });

    // Event für Input-Feldänderungen, um korrekte Maskierung sicherzustellen
    INPUT.addEventListener("input", () => {
        if (INPUT.type === "password") {
            // Stellen Sie sicher, dass die Punktdarstellung aktualisiert wird
            const maskedValue = new Array(INPUT.value.length).fill("•").join("");
            PROXY.textContent = maskedValue;
        }
    });

    // Füge CSS für bessere visuelle Rückmeldung hinzu, aber ohne blauen Rand
    const style = document.createElement('style');
    style.textContent = `
        #password {
            transition: border-color 0.3s ease;
            outline: none; /* Entfernt den Standard-Fokus-Rand */
        }
        #password:focus {
            outline: none; /* Entfernt den Standard-Fokus-Rand */
            box-shadow: none; /* Entfernt jeden möglichen Schatten */
            border-color: inherit; /* Behält die ursprüngliche Rahmenfarbe bei */
        }
        #toggle-password {
            cursor: pointer;
            transition: opacity 0.3s ease;
        }
        #toggle-password:hover {
            opacity: 0.8;
        }
        #toggle-password:active {
            opacity: 0.6;
        }
    `;
    document.head.appendChild(style);
});