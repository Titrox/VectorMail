# Frontend – VectorMail

Dies ist das **Frontend** des **VectorMail E-Mail-Klassifizierungsprojekts**. Es bietet eine interaktive Oberfläche für Benutzer, um E-Mail-Texte einzugeben und deren Klassifizierungsergebnisse in Echtzeit zu sehen. Eine dynamische Anzeige der Klassifizierungswahrscheinlichkeiten reagiert visuell (z.B. durch Farbcodierung), und Benutzer können eigene E-Mail-Texte eingeben oder auf Beispiels-E-Mails zugreifen.

---

## Tech Stack

- **Vue 3** – Modernes JavaScript-Framework
- **Vite** – Schnelles Build-Tool und Entwicklungsserver
- **JavaScript / HTML / CSS**

---

## Voraussetzungen

Bevor Sie das Frontend ausführen, stellen Sie sicher, dass Folgendes auf Ihrem System installiert ist:

- [Node.js](https://nodejs.org/) (Version **16+** empfohlen)
- npm (wird mit Node.js geliefert)

Überprüfen Sie die Versionen mit:

```bash
node -v
npm -v
``` 

---

## Erste Schritte

1. Navigieren Sie zum Frontend-Ordner:
```bash
cd frontend
``` 

2. Installieren Sie die Abhängigkeiten:
```bash
npm install
``` 

3. Starten Sie den Entwicklungsserver:
```bash
npm run dev
```

4. Greifen Sie auf die Anwendung zu:

Nach dem Start des Entwicklungsservers stellt Vite eine lokale Entwicklungs-URL bereit (typischerweise http://localhost:5173). Die genaue URL wird in Ihrem Terminal angezeigt.



---

## Funktionen
- Echtzeit-Anzeige der Klassifizierungswahrscheinlichkeiten für verschiedene E-Mail-Kategorien
- Eingabe benutzerdefinierter E-Mail-Texte zur Klassifizierung
- Visualisierung der Klassifizierungszuversicht durch farbcodierte Labels
- Responsive Benutzeroberfläche für die E-Mail-Eingabe und Ergebnisanzeige
- Durchblättern von Beispiel-E-Mails

---


## Hinweise
- Stellen Sie sicher, dass das Backend (z.B. Spring Boot oder Flask in Docker) läuft und über die REST API zugänglich ist.
- Wenn Sie das Backend lokal betreiben, konfigurieren Sie gegebenenfalls CORS oder verwenden Sie einen lokalen Proxy.





