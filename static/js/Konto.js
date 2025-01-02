// JavaScript für das Dropdown-Menü
document.getElementById('userMenuButton').addEventListener('click', function () {
    var menu = document.getElementById('dropdownMenu');
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
});

// Klicken außerhalb des Menüs schließt es
window.addEventListener('click', function (event) {
    var menu = document.getElementById('dropdownMenu');
    var button = document.getElementById('userMenuButton');
    if (!button.contains(event.target) && !menu.contains(event.target)) {
        menu.style.display = 'none';
    }
});