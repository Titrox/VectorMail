import openai
from openai import OpenAI
import json
import time


client = OpenAI(api_key="sk-...")  # Your API Key

label = ""   

base_prompt = f"""

Bitte generiere **jeweils genau 10 E-Mails** für das folgende Label im folgenden JSON-Format:

[
{{
"label": "{label}",
"text": "<realistische E-Mail in deutscher Sprache>"
}},
{{
"label": "{label}",
"text": "<realistische E-Mail in deutscher Sprache>"
}},
{{
"label": "{label}",
"text": "<realistische E-Mail in deutscher Sprache>"
}},
{{
"label": "{label}",
"text": "<realistische E-Mail in deutscher Sprache>"
}},
{{
"label": "{label}",
"text": "<realistische E-Mail in deutscher Sprache>"
}},
...
]


---

## Regeln:

1. Die E-Mail soll **formell, aber alltagsnah** klingen – wie eine echte Nachricht von Privatpersonen oder Kunden.
2. Der E-Mailtext soll **3–4 Sätze** lang sein, in natürlichem Deutsch.
3. Verwende **keine sensiblen Daten** wie echte Adressen, Telefonnummern oder reale Versicherungsnummern.
4. Die E-Mail soll **thematisch zum jeweiligen Schadenstyp passen**, ohne zu ausschweifend oder künstlich zu wirken.
5. Verwende **normale, höfliche Sprache**, gerne mit kleinen individuellen Variationen im Ausdruck.
6. Gib **nur die Keys `label` und `text`** zurück – keine Metadaten, Überschriften oder Kommentare.
7. Ignoriere Begrüßungen und Verabschiedungen innerhalb der E-Mail, nur Szenarien.
8. Jede E-Mail beginnt mit einem [BEGIN_EMAIL]-Token der die Begrüßung ersetzz
9. Jede E-Mail endet mit [END_EMAIL]-Token der die Verabschiedung ersetzt

---

## Kategorie-Beispiele:

- `"kfz-schaden"` → z.B. Unfall, Blechschaden, Wildunfall
- `"hausrat-schaden"` → z.B. Einbruch, Wasserschaden, Brandschaden
- `"haftpflichtschaden"` → z.B. versehentliche Beschädigung fremder Dinge
- `"reiseschaden"` → z.B. Gepäckverlust, Stornierung, Krankheit im Urlaub
- `"tierkrankheit"` → z.B. OP beim Haustier, Tierarztrechnung

---

## Thematische Richtlinien für jede Kategorie:

### Kfz-Schaden:
- **Betreff:** Schäden an Autos oder Motorrädern
- **Typische Begriffe:** „Unfall“, „Fahrzeug“, „Blechschaden“, „Wild“, „Polizei“

### Hausrat-Schaden:
- **Betreff:** Schäden am Inventar in Wohnung oder Haus
- **Typische Begriffe:** „Einbruch“, „Rohrbruch“, „Fernseher“, „gestohlen“

### Haftpflichtschaden:
- **Betreff:** Absender hat Dritten Schaden zugefügt
- **Typische Begriffe:** „versehentlich“, „mein Kind“, „beschädigt“, „Nachbar“

### Reiseschaden:
- **Betreff:** Probleme im Urlaub, z.B. Verlust, Krankheit
- **Typische Begriffe:** „Koffer“, „Flug“, „Storno“, „Rechnung“, „Ausland“

### Tierkrankheit:
- **Betreff:** Tierarztkosten, Behandlungen von Haustieren
- **Typische Begriffe:** „Hund“, „Katze“, „OP“, „Tierarzt“, „Rechnung“
"""


all_label = [
    "kfz-schaden",
    "hausrat-schaden",
    "haftpflichtschaden",
    "reiseschaden",
    "tierkrankheit"
]

prev_text = ""
label = ""

def generate_email():
    global prev_text

    response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": f"Du bist ein Generator für realistische, formelle E-Mails an eine Versicherung. Gib nur JSON zurück. Deine Antwort soll von der zuvorigen Antwort: {prev_text} abweichen"},
        {"role": "user", "content": base_prompt + f"LABEL = {label}"}
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


num_iterations = 10 # * 50 = E-Mails 
all_emails = []

for curr_label in all_label:

    label = curr_label

    for i in range(num_iterations):
        email = generate_email()
        if email:
            all_emails.append(email)
        time.sleep(1.2) 
    


with open(f"emails_generated.json", "w", encoding="utf-8") as f:
    json.dump(all_emails, f, indent=2, ensure_ascii=False)

print(f"{len(all_emails) * 10} E-Mails erfolgreich gespeichert.")