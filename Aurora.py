from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Lade das vortrainierte GPT-2 Modell und den Tokenizer
model_name = "gpt2"  # Standard GPT-2 Modell
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)


# Funktion zur Generierung von Text
def generate_text(prompt, max_length=100):
    # Tokenize die Eingabeaufforderung
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    # Generiere eine Antwort
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2, top_p=0.95,
                             temperature=0.7)

    # Dekodiere die Antwort und gebe sie aus
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# Beispiel-Konversation: Präsentation von Aurora als KI
def aurora_conversation():
    print("Willkommen bei Aurora! Du kannst mit mir sprechen, und ich werde dir antworten. Stelle mir jede Frage.")
    print("Wenn du die Konversation beenden möchtest, gib einfach 'exit' ein.")

    while True:
        user_input = input("Du: ")

        if user_input.lower() == "exit":
            print("Aurora: Auf Wiedersehen! Bis zum nächsten Mal.")
            break

        prompt = f"Du bist Aurora, eine fortschrittliche KI, die darauf spezialisiert ist, menschenähnliche Konversationen zu führen. Beantworte folgende Frage:\n{user_input}\n"
        response = generate_text(prompt)

        # Präsentation der Antwort unter dem Namen „Aurora“
        print(f"Aurora: {response}")


# Starte die Konversation
if __name__ == "__main__":
    aurora_conversation()