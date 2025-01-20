// Einblenden der Sektionen beim Scrollen
document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section');

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