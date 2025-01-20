document.addEventListener('DOMContentLoaded', function () {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    // Funktion zur Handhabung der Tabs
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Entferne 'active' Klasse von allen Tabs und Pane-Inhalten
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Füge 'active' Klasse hinzu für den angeklickten Tab und den zugehörigen Pane
            this.classList.add('active');
            const activeTab = this.id.replace('tab-', '');
            const activePane = document.getElementById(activeTab);
            activePane.classList.add('active');

            // Erscheinungseffekt für die Unterkategorien, speziell beim "Added"-Tab
            if (activeTab === 'added') {
                showAddedItems();
            }
        });
    });

    // Standardmäßig den "Small Bug Fix"-Tab aktivieren
    document.getElementById('tab-small').click();

    // Hover-Effekt für die Unterkategorien
    const categories = document.querySelectorAll('.tab-pane .fix-list ul li');
    categories.forEach(category => {
        category.addEventListener('mouseenter', () => {
            category.style.transform = 'translateX(10px)';
            category.style.transition = 'transform 0.3s ease';
        });
        category.addEventListener('mouseleave', () => {
            category.style.transform = 'translateX(0)';
        });
    });

    // Funktion zum Anzeigen der "Added"-Items mit einer Verzögerung (Erscheinungseffekt)
    function showAddedItems() {
        const addedItems = document.querySelectorAll('#added .fix-list ul li');
        addedItems.forEach((item, index) => {
            // Verzögerung je nach Index
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
                item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            }, index * 300); // Verzögerung von 300ms pro Item
        });
    }

    // Erscheinungseffekt für die gesamte Seite
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 1s ease-in-out';
    window.setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100); // Verzögerung, um die Transition auszulösen
});