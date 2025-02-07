document.addEventListener("DOMContentLoaded", function() {
    gsap.registerPlugin(ScrambleTextPlugin, MorphSVGPlugin);

    const BLINK_SPEED = 0.075;
    const TOGGLE_SPEED = 0.125;
    const ENCRYPT_SPEED = 1;

    let busy = false;

    // EYE wird nicht mehr benötigt, da wir die Animation nicht ändern
    const TOGGLE_PASSWORD = document.getElementById("toggle-password");
    const TOGGLE_CONFIRM_PASSWORD = document.getElementById("toggle-confirm-password");

    const INPUT_PASSWORD = document.getElementById("password");
    const INPUT_CONFIRM_PASSWORD = document.getElementById("confirm-password");

    const PROXY_PASSWORD = document.createElement('div');
    const PROXY_CONFIRM_PASSWORD = document.createElement('div');

    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~,.<>?/;":][}{+_)(*&^%$#@!±=-§';

    // Blinken des Augen-Elements (dies bleibt, aber es wird nicht genutzt)
    let blinkTl;
    const BLINK = () => {
        const delay = gsap.utils.random(2, 8);
        const duration = BLINK_SPEED;
        const repeat = Math.random() > 0.5 ? 3 : 1;
        blinkTl = gsap.timeline({
            delay,
            onComplete: () => BLINK(),
            repeat,
            yoyo: true
        })
            .to('.lid--upper', { morphSVG: '.lid--lower', duration })
            .to('#eye-open path', { morphSVG: '#eye-closed path', duration }, 0);
    };

    BLINK(); // Initialisieren des Blinkens

    // Funktion für das Toggle für Passwort
    const togglePassword = (input, toggle, proxy) => {
        if (busy) return;
        const isText = input.matches('[type=password]');
        const val = input.value;
        busy = true;
        toggle.setAttribute('aria-pressed', isText);
        const eyeIcon = toggle.querySelector('i');

        if (isText) {
            eyeIcon.classList.remove("fa-eye");
            eyeIcon.classList.add("fa-eye-slash");  // Symbol für verborgenes Passwort

            gsap.timeline({
                onComplete: () => {
                    busy = false;
                }
            })
                .to('.lid--upper', { morphSVG: '.lid--lower', TOGGLE_SPEED })
                .to('#eye-open path', { morphSVG: '#eye-closed path', TOGGLE_SPEED }, 0)
                .to(proxy, {
                    duration: ENCRYPT_SPEED,
                    onStart: () => {
                        input.type = 'text';
                    },
                    onComplete: () => {
                        proxy.innerHTML = '';
                        input.value = val;
                    },
                    scrambleText: {
                        chars,
                        text: input.value.charAt(input.value.length - 1) === ' ' ? `${input.value.slice(0, input.value.length - 1)}${chars.charAt(Math.floor(Math.random() * chars.length))}` : input.value
                    },
                    onUpdate: () => {
                        const len = val.length - proxy.innerText.length;
                        input.value = `${proxy.innerText}${new Array(len).fill('•').join('')}`;
                    }
                }, 0);
        } else {
            eyeIcon.classList.remove("fa-eye-slash");
            eyeIcon.classList.add("fa-eye");  // Symbol für sichtbares Passwort

            gsap.timeline({
                onComplete: () => {
                    BLINK();
                    busy = false;
                }
            })
                .to('.lid--upper', { morphSVG: '.lid--upper', TOGGLE_SPEED })
                .to('#eye-open path', { morphSVG: '#eye-open path', TOGGLE_SPEED }, 0)
                .to(proxy, {
                    duration: ENCRYPT_SPEED,
                    onComplete: () => {
                        input.type = 'password';
                        input.value = val;
                        proxy.innerHTML = '';
                    },
                    scrambleText: {
                        chars,
                        text: new Array(input.value.length).fill('•').join('')
                    },
                    onUpdate: () => {
                        input.value = `${proxy.innerText}${val.slice(proxy.innerText.length)}`;
                    }
                }, 0);
        }
    };

    // Event-Listener für das Toggle der Passwörter
    TOGGLE_PASSWORD.addEventListener('click', () => togglePassword(INPUT_PASSWORD, TOGGLE_PASSWORD, PROXY_PASSWORD));
    TOGGLE_CONFIRM_PASSWORD.addEventListener('click', () => togglePassword(INPUT_CONFIRM_PASSWORD, TOGGLE_CONFIRM_PASSWORD, PROXY_CONFIRM_PASSWORD));

    // Verhindern des Formularabsendens
    const FORM = document.querySelector('form');
    FORM.addEventListener('submit', event => event.preventDefault());
});