document.addEventListener('DOMContentLoaded', function() {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = 'Passwort wurde in die Zwischenablage kopiert!';
    document.body.appendChild(notification);

    // Copy functionality
    const copyButton = document.getElementById('copy-password');
    const copyIcon = document.getElementById('copy-icon');

    copyButton.addEventListener('click', async function() {
        const passwordInput = document.getElementById('generated-password');

        try {
            await navigator.clipboard.writeText(passwordInput.value);

            // Change icon to check
            copyIcon.classList.remove('fa-copy');
            copyIcon.classList.add('fa-check');

            // Show notification
            notification.classList.add('show');

            // Reset after 2 seconds
            setTimeout(() => {
                copyIcon.classList.remove('fa-check');
                copyIcon.classList.add('fa-copy');
                notification.classList.remove('show');
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    });
});