// Einblenden der Sektionen beim Laden der Seite und Scrollen
document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section');

    // Direkt beim Laden der Seite den Effekt anwenden
    sections.forEach(function(section) {
        const rect = section.getBoundingClientRect();
        if (rect.top <= window.innerHeight && rect.bottom >= 0) {
            section.classList.add('in-view');
        }
    });

    // Einblenden der Sektionen beim Scrollen
    window.addEventListener('scroll', function() {
        sections.forEach(function(section) {
            const rect = section.getBoundingClientRect();
            if (rect.top <= window.innerHeight && rect.bottom >= 0) {
                section.classList.add('in-view');
            } else {
                section.classList.remove('in-view');
            }
        });
    });
});