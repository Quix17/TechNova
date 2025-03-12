document.getElementById('bugReportForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    try {
        let response = await fetch('/submit_bug', {
            method: 'POST',
            body: formData
        });

        let result = await response.json();
        alert(result.message);
        this.reset();
    } catch (error) {
        console.error("Fehler beim Senden des Bug-Reports:", error);
        alert("Es gab ein Problem beim Senden des Bug-Reports.");
    }
});
