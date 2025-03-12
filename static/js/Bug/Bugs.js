document.addEventListener("DOMContentLoaded", function () {
    const bugItems = document.querySelectorAll('.bug-item');
    const statValues = document.querySelectorAll(".stat-value");

    // 🔹 Funktion zum Hochzählen der Statistiken
    function animateCount(element, targetValue, duration = 2000) {
        let startValue = 0;
        let startTime = performance.now();

        function updateCounter(currentTime) {
            let elapsedTime = currentTime - startTime;
            let progress = Math.min(elapsedTime / duration, 1);

            let currentValue = Math.floor(progress * targetValue);
            element.textContent = currentValue;

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = targetValue; // Endwert sicherstellen
            }
        }

        requestAnimationFrame(updateCounter);
    }

    // 🔹 Starte die Animation für jede Statistik-Zahl
    statValues.forEach(stat => {
        let targetValue = parseFloat(stat.textContent);
        stat.textContent = "0";
        animateCount(stat, targetValue);
    });

    // 🔹 Funktion, um die Bugs nacheinander erscheinen zu lassen
    function animateBugs() {
        bugItems.forEach((item, index) => {
            setTimeout(() => {
                item.style.transition = "opacity 0.6s ease, transform 0.6s ease";
                item.style.opacity = 1;
                item.style.transform = "translateY(0)";
            }, index * 500);
        });
    }

    // 🔹 Hover-Effekt für das Verschieben nach rechts
    bugItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = "translateX(10px)";
        });

        item.addEventListener('mouseleave', () => {
            item.style.transform = "translateX(0)";
        });
    });

    // 🔹 Starte beide Animationen
    animateBugs();
});
