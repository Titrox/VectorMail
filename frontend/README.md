# Frontend – VectorMail

This is the frontend of the VectorMail email classification project. It provides an interactive interface for users to input email texts and see their classification results in real time. A dynamic display of classification probabilities reacts visually (e.g., through color-coding), and users can enter their own email texts or access example emails.
---

## Tech Stack

- **Vue 3** – Modern JavaScript-Framework
- **Vite** – Fast build tool and development server
- **JavaScript / HTML / CSS**

---

## Prerequisites
Before running the frontend, ensure the following are installed on your system:

Node.js (version 16+ recommended)
npm (comes with Node.js)
Check versions with:

```bash
node -v
npm -v
``` 

---

## Getting Started

1. Navigate to the frontend folder:
```bash
cd frontend
``` 

2. Install the dependecies:
```bash
npm install
``` 

3. Start the development server:
```bash
npm run dev
```

4. Access the application:

After starting the dev server, Vite will provide a local development URL (typically http://localhost:5173). The exact URL will appear in your terminal.



---

## Features
- Real-time display of classification probabilities for various email categories
- Input of custom email texts for classification
- Visualization of classification confidence through color-coded labels
- Responsive user interface for email input and result display
- Browse of example emails

---


## Notes
- Make sure the backend (e.g., Spring Boot or Flask in Docker) is running and accessible via REST API.
- If you're running the backend locally, configure CORS or use a local proxy if needed.





