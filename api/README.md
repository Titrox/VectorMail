# VectorMail API

This is the backend service for the VectorMail application. It is built using Spring Boot and acts as a bridge between the Vue.js frontend and the Python-based email classification engine.

---

## Getting Started

To run the backend service:

1.  Navigate to the `api` directory from the project root:
    ```bash
    cd api
    ```
2.  Run the application using Maven:
    ```bash
    mvn spring-boot:run
    ```

The backend will start and be available at [http://localhost:8080](http://localhost:8080).

---

## API Endpoints

The primary endpoint provided by this service is:

### POST `/evaluate-email`

-   **Purpose**: Receives an email text (as a JSON string) from the frontend, forwards it to the Python classification engine for analysis, and then returns the engine's response.
-   **Request Body**:
    ```json
    "email text to classify"
    ```
    (Note: The body is a raw JSON string, ensure `Content-Type: application/json` is set)
-   **Response**: Probabilities of all defined labels.

---

## CORS Configuration

Cross-Origin Resource Sharing (CORS) is configured to allow requests from the frontend service:

-   **Allowed Origins**: `http://localhost:5173` (default Vue.js development server)
-   **Allowed HTTP Methods**: `GET, POST, PUT, DELETE, OPTIONS`
-   **Allowed Headers**: All (`*`)
-   **Credentials Allowed**: `true`

This configuration is handled in `src/main/java/com/example/VectorMail/config/CorsConfig.java`.

---

## Communication with Python Service

The API communicates with the Python classification engine, which is expected to be running as a Flask service.

-   The Python service endpoint is hardcoded as: `http://localhost:5000/`
-   The `/evaluate-email` endpoint in this API forwards requests to the `/evaluate-email` endpoint on the Python service.

---

## Project Structure

A simplified overview of the `api` module structure:

```
api/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/VectorMail/
│   │   │       ├── config/
│   │   │       │   └── CorsConfig.java         # CORS configuration
│   │   │       ├── controller/
│   │   │       │   └── ModelController.java    # Handles incoming API requests
│   │   │       └── VectorMailApplication.java  # Main Spring Boot application class
│   │   └── resources/
│   │       └── application.properties      # Spring Boot application settings
├── pom.xml                               # Maven project configuration
└── README.md                             # This file
```

---

## Requirements

-   Java 17+
-   Maven
```
