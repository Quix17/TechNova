const express = require('express');
const bodyParser = require('body-parser');
const { OpenAI } = require('openai'); // Die neue Import-Methode
const cors = require('cors');
const path = require('path');
const app = express();
const port = 3000;

// Dein neuer OpenAI API-Schlüssel
const openaiAPIKey = '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';

// Konfiguriere OpenAI
const openai = new OpenAI({
  apiKey: openaiAPIKey,
  baseURL: 'https://api.openai.com/v1', // Optional, wenn du den Standard-Endpunkt verwenden möchtest
});

// Middleware
app.use(cors()); // CORS für externe Anfragen aktivieren
app.use(bodyParser.json()); // JSON-Daten parsen

// Statische Dateien für Frontend bereitstellen
app.use(express.static(path.join(__dirname, 'public')));

// Endpunkt für Anfragen an OpenAI
app.post('/ask', async (req, res) => {
  const prompt = req.body.prompt; // Holen des Benutzer-Prompts

  if (!prompt) {
    return res.status(400).send('Fehlender Prompt. Bitte gib einen Prompt an.');
  }

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo', // Modell, das verwendet werden soll
      messages: [
        { role: 'system', content: 'Du bist Aurora, ein fortschrittlicher KI-Chatbot.' },
        { role: 'user', content: prompt },
      ],
      max_tokens: 150,
      temperature: 0.7,
    });

    // Sende die Antwort zurück an den Client
    const reply = response.choices[0].message.content.trim();
    res.json({ reply: reply });
  } catch (error) {
    console.error('Fehler bei der Anfrage:', error);
    res.status(500).send('Fehler bei der Anfrage an OpenAI.');
  }
});

// Starte den Server
app.listen(port, () => {
  console.log(`Server läuft auf http://localhost:${port}`);
});