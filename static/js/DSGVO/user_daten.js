document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll('.data-item').forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.backgroundColor = 'rgba(255, 255, 255, 0.15)';
            item.style.transition = 'background 0.3s ease-in-out';
        });
        item.addEventListener('mouseleave', () => {
            item.style.backgroundColor = '';
        });
    });
});
