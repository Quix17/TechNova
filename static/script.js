// Dokument laden
document.addEventListener('DOMContentLoaded', function () {

    // Navigation Scroll
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            document.getElementById(targetId).scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Sticky Header
    const header = document.querySelector('header');
    const headerOffset = header.offsetTop;

    window.addEventListener('scroll', function () {
        if (window.pageYOffset > headerOffset) {
            header.classList.add('sticky');
        } else {
            header.classList.remove('sticky');
        }
    });

    // Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const menu = document.querySelector('.nav-links');

    menuToggle.addEventListener('click', function () {
        menu.classList.toggle('active');
    });

    // Testimonial Slider
    const testimonialItems = document.querySelectorAll('.testimonial-item');
    let testimonialIndex = 0;

    function showTestimonial(index) {
        testimonialItems.forEach((item, i) => {
            item.style.display = (i === index) ? 'block' : 'none';
        });
    }

    function nextTestimonial() {
        testimonialIndex = (testimonialIndex + 1) % testimonialItems.length;
        showTestimonial(testimonialIndex);
    }

    function prevTestimonial() {
        testimonialIndex = (testimonialIndex - 1 + testimonialItems.length) % testimonialItems.length;
        showTestimonial(testimonialIndex);
    }

    document.querySelector('.next-testimonial').addEventListener('click', nextTestimonial);
    document.querySelector('.prev-testimonial').addEventListener('click', prevTestimonial);

    // Initialize first testimonial
    showTestimonial(testimonialIndex);

    // Scroll Animations for Sections
    const sections = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.5 });

    sections.forEach(section => observer.observe(section));

    // Form Validation
    const form = document.querySelector('.contact-form');
    const nameField = form.querySelector('input[name="name"]');
    const emailField = form.querySelector('input[name="email"]');
    const messageField = form.querySelector('textarea[name="message"]');

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        let valid = true;

        if (nameField.value.trim() === '') {
            valid = false;
            nameField.classList.add('error');
        } else {
            nameField.classList.remove('error');
        }

        if (emailField.value.trim() === '' || !emailField.value.includes('@')) {
            valid = false;
            emailField.classList.add('error');
        } else {
            emailField.classList.remove('error');
        }

        if (messageField.value.trim() === '') {
            valid = false;
            messageField.classList.add('error');
        } else {
            messageField.classList.remove('error');
        }

        if (valid) {
            form.submit();
        } else {
            alert('Bitte füllen Sie alle Felder korrekt aus.');
        }
    });

    // Smooth Scroll to Top Button
    const scrollTopButton = document.querySelector('.scroll-to-top');

    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 200) {
            scrollTopButton.classList.add('visible');
        } else {
            scrollTopButton.classList.remove('visible');
        }
    });

    scrollTopButton.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Lightbox Gallery
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.querySelector('.lightbox');
    const lightboxImage = document.querySelector('.lightbox-image');
    const closeLightbox = document.querySelector('.lightbox-close');

    galleryItems.forEach(item => {
        item.addEventListener('click', function () {
            const imgSrc = this.querySelector('img').getAttribute('src');
            lightboxImage.setAttribute('src', imgSrc);
            lightbox.classList.add('open');
        });
    });

    closeLightbox.addEventListener('click', function () {
        lightbox.classList.remove('open');
    });

    // Animation on Scroll
    const scrollElements = document.querySelectorAll('.scroll-animate');
    window.addEventListener('scroll', function () {
        scrollElements.forEach(element => {
            const position = element.getBoundingClientRect().top;
            if (position < window.innerHeight - 100) {
                element.classList.add('fade-in');
            }
        });
    });

    // Parallax Effect
    const parallaxElements = document.querySelectorAll('.parallax');

    window.addEventListener('scroll', function () {
        parallaxElements.forEach(element => {
            let offset = window.pageYOffset;
            element.style.backgroundPositionY = (offset * 0.3) + "px";
        });
    });

    // Countdown Timer
    const countdown = document.querySelector('.countdown');
    const targetDate = new Date('December 31, 2024 23:59:59').getTime();

    function updateCountdown() {
        const now = new Date().getTime();
        const timeLeft = targetDate - now;

        if (timeLeft <= 0) {
            countdown.innerHTML = 'Event Started';
            clearInterval(countdownInterval);
        } else {
            const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
            const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
            countdown.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }
    }

    const countdownInterval = setInterval(updateCountdown, 1000);

    // Scroll Reveal for Testimonials
    const testimonialItems2 = document.querySelectorAll('.testimonial-item');
    testimonialItems2.forEach(item => {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, { threshold: 0.5 });
        revealObserver.observe(item);
    });

    // Toggle Light Mode/Dark Mode
    const darkModeToggle = document.querySelector('.dark-mode-toggle');
    const body = document.body;

    darkModeToggle.addEventListener('click', function () {
        body.classList.toggle('dark-mode');
        localStorage.setItem('dark-mode', body.classList.contains('dark-mode'));
    });

    // Remember dark mode preference
    if (localStorage.getItem('dark-mode') === 'true') {
        body.classList.add('dark-mode');
    }

    // Hero Slider
    let heroSlideIndex = 0;
    const heroSlides = document.querySelectorAll('.hero-slide');

    function showHeroSlide(index) {
        heroSlides.forEach((slide, i) => {
            slide.style.display = (i === index) ? 'block' : 'none';
        });
    }

    function nextHeroSlide() {
        heroSlideIndex = (heroSlideIndex + 1) % heroSlides.length;
        showHeroSlide(heroSlideIndex);
    }

    setInterval(nextHeroSlide, 5000);

    // Initialize hero slider
    showHeroSlide(heroSlideIndex);
});
// Smooth Scroll for Navigation
const links = document.querySelectorAll('nav a');

links.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').slice(1);
        const targetElement = document.getElementById(targetId);

        window.scrollTo({
            top: targetElement.offsetTop - 100, // Adjust for header height
            behavior: 'smooth'
        });
    });
});

// Optional: Animation for sections as they enter the viewport
const sections = document.querySelectorAll('.shape-box');

const observeOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.2
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        } else {
            entry.target.classList.remove('visible');
        }
    });
}, observeOptions);

sections.forEach(section => {
    observer.observe(section);
});
