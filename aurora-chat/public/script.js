// Event Listener für den Absende-Button
document.getElementById('sendButton').addEventListener('click', async () => {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === '') return;

    // Zeige die Nachricht des Nutzers im Chat-Fenster
    appendMessage('Du', userInput);

    // Leere das Eingabefeld
    document.getElementById('userInput').value = '';

    try {
        // Rufe die Antwort von Aurora KI ab
        const response = await getAuroraResponse(userInput);

        // Zeige die Antwort von Aurora im Chat-Fenster
        appendMessage('Aurora', response);
    } catch (error) {
        appendMessage('Aurora', 'Entschuldigung, es gab ein Problem mit der Anfrage.');
        console.error('Error fetching response:', error);
    }
});

// Diese Funktion fügt Nachrichten zum Chat hinzu
function appendMessage(sender, message) {
    const chatBox = document.getElementById('chatBox');
    const messageElement = document.createElement('div');

    messageElement.classList.add(sender.toLowerCase()); // Sender kann "Du" oder "Aurora" sein
    messageElement.textContent = `${sender}: ${message}`;

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;  // Scrollen zum neuesten Beitrag
}

async function getAuroraResponse(prompt) {
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.reply;
}