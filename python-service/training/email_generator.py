import openai
from openai import OpenAI
import json
import time


client = OpenAI(api_key="sk-...")  # Insert your API Key

base_prompt = """

Bitte generiere jeweils genau eine E-Mail für jedes der folgenden Labels im JSON-Array-Format. Stelle sicher, dass das generierte JSON-Array genau fünf E-Mails enthält, eine für jedes der unten aufgeführten Labels in der angegebenen Reihenfolge. Für jedes Label sollte das Szenario **möglichst variiert** sein und die gesamte thematische Bandbreite der aufgeführten Beispiele **ausnutzen**.

[
    {
    "label": "kfz-schaden",
    "text": "<realistische E-Mail in deutscher Sprache>"
    },
    {
    "label": "hausrat-schaden",
    "text": "<realistische E-Mail in deutscher Sprache>"
    },
    {
    "label": "haftpflichtschaden",
    "text": "<realistische E-Mail in deutscher Sprache>"
    },
    {
    "label": "reiseschaden",
    "text": "<realistische E-Mail in deutscher Sprache>"
    },
    {
    "label": "tierkrankheit",
    "text": "<realistische E-Mail in deutscher Sprache>"
    }
]

### Regeln:

1. Die E-Mail soll **formell, aber alltagsnah** klingen – wie eine echte Nachricht von Privatpersonen oder Kunden.
    
2. Der E-Mailtext soll **3–4 Sätze** lang sein, in natürlichem Deutsch.
    
3. Verwende **keine sensiblen Daten** wie echte Adressen, Telefonnummern oder reale Versicherungsnummern.
    
4. Die E-Mail soll **thematisch zum jeweiligen Schadenstyp passen**, ohne zu ausschweifend oder künstlich zu wirken.
    
5. Verwende **normale, höfliche Sprache**, gerne mit kleinen individuellen Variationen im Ausdruck.
    
6. Gib **nur die Keys `label` und `text`** zurück – keine Metadaten, Überschriften oder Kommentare.
    


Bitte beachte die thematischen Richtlinien für jede Kategorie:

#### Kfz-Schaden:

- Betreff: Schäden an Autos oder Motorrädern
    
- Typische Begriffe: „Unfall“, „Fahrzeug“, „Blechschaden“, „Wild“, „Polizei“, **„Hagel“, „Parkplatz“
    

#### Hausrat-Schaden:

- Betreff: Schäden am Inventar in Wohnung oder Haus
    
- Typische Begriffe: „Brand“, „Feuer“, „Rauch“, „Sturm“, „Wasserleitung“**
    

#### Haftpflichtschaden:

- Betreff: Absender hat Dritten Schaden zugefügt
    
- Typische Begriffe: „versehentlich“, „mein Kind“, „beschädigt“, „Nachbar“, **„Haustier“, „Hund verursacht“**
    

#### Reiseschaden:

- Betreff: Probleme im Urlaub, z.B. Verlust, Krankheit
    
- Typische Begriffe:  „Flug“, „Storno“, „Rechnung“, „Ausland“, „Verspätung“, „krank im Urlaub“, „Notfall“**
    

#### Tierkrankheit:

- Betreff: Tierarztkosten, Behandlungen von Haustieren
    
- Typische Begriffe: „Hund“, „Katze“, „OP“, „Tierarzt“, „Rechnung“, **„Krankheit“, „Verletzung“, „Behandlung“**
    
    
"""

prev_text = ""

def generate_email():
    global prev_text

    response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": f"Du bist ein Generator für realistische, formelle E-Mails an eine Versicherung. Gib nur JSON zurück. Deine Antwort soll von der zuvorigen Antwort: {prev_text} abweichen"}, # Define System
        {"role": "user", "content": base_prompt}
    ],
    temperature=0.8
)
    text = response.choices[0].message.content
    

    prev_text = text
    
    try:
        return json.loads(text)
    except:
        print("Fehler beim Parsen der Antwort:")
        print(text)
        return None

# Number of iterations
num_emails = 200
all_emails = []

for i in range(num_emails):
    email = generate_email()
    if email:
        all_emails.append(email)
    time.sleep(1.2) 

with open("emails_generated.json", "w", encoding="utf-8") as f:
    json.dump(all_emails, f, indent=2, ensure_ascii=False)

print(f"{len(all_emails) * 5} E-Mails erfolgreich gespeichert.")