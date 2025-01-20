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
