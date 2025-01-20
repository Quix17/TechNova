document.addEventListener('DOMContentLoaded', () => {
    const faqCategories = document.querySelectorAll('.faq-category');
    const faqItems = document.querySelectorAll('.faq-item');

    // Reinfliegen-Effekt
    const reinFliegenEffect = (element, delay) => {
        element.style.opacity = 0;
        element.style.transform = 'translateY(-20px)';
        element.style.transition = 'transform 0.8s ease, opacity 0.8s ease';
        element.style.transitionDelay = delay + 'ms';

        // Animation nach einer kurzen Verzögerung
        setTimeout(() => {
            element.style.opacity = 1;
            element.style.transform = 'translateY(0)';
        }, delay);
    };

    // Hover-Effekt
    const addHoverEffect = (element) => {
        element.addEventListener('mouseover', () => {
            element.style.transform = 'translateY(-5px)';
            element.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
            element.style.cursor = 'pointer';
        });

        element.addEventListener('mouseout', () => {
            element.style.transform = 'translateY(0)';
            element.style.boxShadow = 'none';
        });
    };

    // Ein-/Ausklappen der Antworten
    const toggleAnswer = (event) => {
        const answer = event.target.nextElementSibling; // Nächstes Element ist die Antwort
        if (answer.style.display === 'none' || answer.style.display === '') {
            answer.style.display = 'block'; // Antwort anzeigen
        } else {
            answer.style.display = 'none'; // Antwort ausblenden
        }
    };

    // Funktion zum Auslösen der Animation beim Scrollen
    const handleScrollAnimation = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                reinFliegenEffect(entry.target, 0); // Animation auslösen
                observer.unobserve(entry.target); // Stoppt die Beobachtung, sobald die Animation ausgeführt wurde
            }
        });
    };

    // IntersectionObserver für Scroll-Animation
    const observer = new IntersectionObserver(handleScrollAnimation, {
        threshold: 0.5, // Auslösen der Animation, wenn 50% des Elements sichtbar sind
    });

    // Alle FAQ-Elemente nach und nach animieren
    faqCategories.forEach((category, index) => {
        reinFliegenEffect(category, index * 200); // Verzögerung für Kategorien
        addHoverEffect(category); // Hover-Effekt für die Kategorien

        // Event Listener für das Ein-/Ausklappen der Kategorien
        category.addEventListener('click', toggleAnswer);

        // Beobachten, ob das Element in den Viewport kommt
        observer.observe(category);
    });

    faqItems.forEach((item, index) => {
        reinFliegenEffect(item, (faqCategories.length + index) * 200); // Verzögerung für Items
        addHoverEffect(item.querySelector('.faq-question')); // Hover-Effekt für die Fragen

        // Event Listener für das Ein-/Ausklappen der Antworten
        const questionButton = item.querySelector('.faq-question');
        questionButton.addEventListener('click', toggleAnswer);

        // Beobachten, ob das Element in den Viewport kommt
        observer.observe(item);
    });
});
