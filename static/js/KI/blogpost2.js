document.addEventListener('DOMContentLoaded', function() {
    // Google Fonts laden
    const fontLink = document.createElement('link');
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap';
    fontLink.rel = 'stylesheet';
    document.head.appendChild(fontLink);

    // Smooth Scroll für Navigation
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            window.scrollTo({
                top: targetSection.offsetTop,
                behavior: 'smooth'
            });

            // Aktive Klasse setzen
            navLinks.forEach(link => link.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Parallax-Effekt für Hintergründe hinzufügen
    const sections = document.querySelectorAll('section');

    sections.forEach(section => {
        // Parallax Hintergrund erstellen
        const parallaxBg = document.createElement('div');
        parallaxBg.classList.add('parallax-bg');
        section.appendChild(parallaxBg);
    });

    // Scroll-Animation für Elemente
    const animateOnScroll = () => {
        const triggerBottom = window.innerHeight * 0.8;

        // Sections animieren
        document.querySelectorAll('.section-inner').forEach(section => {
            const sectionTop = section.getBoundingClientRect().top;

            if (sectionTop < triggerBottom) {
                section.classList.add('visible');
            }
        });

        // Listenelemente animieren
        document.querySelectorAll('li').forEach((item, index) => {
            const itemTop = item.getBoundingClientRect().top;

            if (itemTop < triggerBottom) {
                // Verzögerung für gestaffelte Animation
                setTimeout(() => {
                    item.classList.add('visible');
                }, index * 100);
            }
        });

        // Parallax-Effekt beim Scrollen
        document.querySelectorAll('.parallax-bg').forEach(bg => {
            const section = bg.parentElement;
            const scrollPosition = window.scrollY;
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;

            // Parallax-Effekt nur anwenden, wenn der Abschnitt im Sichtbereich ist
            if (scrollPosition > sectionTop - window.innerHeight &&
                scrollPosition < sectionTop + sectionHeight) {
                const yPos = (scrollPosition - sectionTop) * 0.3;
                bg.style.transform = `translateY(${yPos}px)`;
            }
        });

        // Aktiven Navigationslink aktualisieren
        const currentPos = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (currentPos >= sectionTop && currentPos < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    };

    // Initialen Aufruf und Scroll-Event-Listener
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);

    // Animierte Zeitmarker
    const timeMarkers = document.querySelectorAll('.time-marker');

    timeMarkers.forEach(marker => {
        const originalPosition = marker.style.left || '40px';

        // Float-Animation hinzufügen
        marker.style.animation = 'float 6s ease-in-out infinite';

        // Zufällige Verzögerung für unterschiedliche Bewegungsmuster
        marker.style.animationDelay = `${Math.random() * 2}s`;
    });

    // "Typing"-Effekt für Überschriften
    document.querySelectorAll('.section-header h2').forEach(heading => {
        const text = heading.textContent;
        heading.textContent = '';

        const typeWriter = (text, i = 0) => {
            if (i < text.length) {
                heading.textContent += text.charAt(i);
                i++;
                setTimeout(() => typeWriter(text, i), 50);
            }
        };

        // IntersectionObserver erstellen, um den Effekt auszulösen, wenn die Überschrift sichtbar wird
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        typeWriter(text);
                    }, 300);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(heading);
    });

    // Pulsierender Effekt für Zitate
    const quotes = document.querySelectorAll('.quote');

    quotes.forEach(quote => {
        quote.addEventListener('mouseenter', function() {
            this.style.animation = 'pulse 2s infinite';
        });

        quote.addEventListener('mouseleave', function() {
            this.style.animation = 'none';
        });
    });

    // Dynamische Partikelhintergründe für Abschnitte
    const createParticles = (section, count = 30) => {
        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');

            // Zufällige Größe, Position und Opazität
            const size = Math.random() * 8 + 2;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.opacity = Math.random() * 0.3;

            // Zufällige Animation
            const duration = Math.random() * 20 + 10;
            particle.style.animation = `float ${duration}s ease-in-out infinite`;
            particle.style.animationDelay = `${Math.random() * 5}s`;

            // Farbe je nach Abschnitt
            if (section.id === 'section8') {
                particle.style.background = 'rgba(58, 134, 255, 0.4)';
            } else if (section.id === 'section9') {
                particle.style.background = 'rgba(131, 56, 236, 0.4)';
            } else {
                particle.style.background = 'rgba(255, 0, 110, 0.4)';
            }

            section.appendChild(particle);
        }
    };

    // CSS für Partikel einfügen
    const particleStyles = document.createElement('style');
    particleStyles.textContent = `
    .particle {
      position: absolute;
      border-radius: 50%;
      pointer-events: none;
      z-index: 0;
    }
  `;
    document.head.appendChild(particleStyles);

    // Partikelhintergründe für jeden Abschnitt erstellen
    sections.forEach(section => {
        createParticles(section);
    });

    // Moderne Schwebende Navigationsleiste
    window.addEventListener('scroll', function() {
        const nav = document.querySelector('nav');

        if (window.scrollY > 100) {
            nav.style.padding = '15px';
            nav.style.background = 'rgba(26, 26, 46, 0.95)';
            nav.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.2)';
        } else {
            nav.style.padding = '20px';
            nav.style.background = 'rgba(26, 26, 46, 0.8)';
            nav.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.15)';
        }
    });

    // Begrüßungsanimation beim Laden der Seite
    const welcomeAnimation = () => {
        // Fade-in für nav items
        document.querySelectorAll('.nav-item').forEach((item, index) => {
            item.style.opacity = '0';
            item.style.animation = `fadeIn 0.5s forwards ${index * 0.2}s`;
        });

        // Erstes sichtbares Section animieren
        const firstSection = document.querySelector('section');
        firstSection.querySelector('.section-inner').classList.add('visible');

        // Erste Listen-Elemente animieren
        firstSection.querySelectorAll('li').forEach((item, index) => {
            setTimeout(() => {
                item.classList.add('visible');
            }, 1000 + (index * 100));
        });
    };

    // Begrüßungsanimation starten
    welcomeAnimation();
});