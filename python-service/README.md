# Python Classification Service - VectorMail

This service is a core component of the VectorMail project, responsible for classifying email texts. It utilizes BERT to predict the category of an email. The service is built with Flask and can be run as a standalone server or as a Docker container.

---

## Getting Started

There are two primary ways to run this service: directly using Python or as a Docker container.

### 1. Running with Python (Directly)

**Prerequisites:**
*   Python 3.x
*   pip (Python package installer)

**Setup:**
1.  Navigate to the `python-service` directory:
    ```bash
    cd python-service
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

**Running the Server:**
Once dependencies are installed, you can start the Flask server:
    ```bash
    python flask_server.py
    ```
The server will start on `http://localhost:5000` by default.

### 2. Running with Docker

**Prerequisites:**
*   Docker installed and running.

**Building and Running the Container:**
The service can be built and run using Docker Compose from the **root directory** of the VectorMail project.
1.  Ensure you are in the root `VectorMail/` directory.
2.  Build and start the service:
    ```bash
    docker-compose up --build python-service
    ```
    If you want to run all services defined in `docker-compose.yml` (which might include this python-service):
    ```bash
    docker-compose up --build
    ```
This will build the Docker image for the `python-service` (if not already built) and start a container, this might take some time. The service within the container will be accessible on port 5000 as configured in `docker-compose.yml` and the `Dockerfile`.

---

## API Endpoint

The service provides a single API endpoint for email classification:

### POST `/evaluate-email`

*   **Purpose**: Receives an email text, classifies it using the machine learning model, and returns the predicted probabilities for defined categories.
*   **Request**:
    *   Method: `POST`
    *   Body: A JSON string containing the email text to be classified.
        ```json
        "Your email text goes here..."
        ```
    *   Headers: `Content-Type: application/json`
*   **Response**:
    *   A JSON object containing the classification probabilities (as percentages, rounded to two decimal places) for predefined categories.
        ```json
        {
          "Hausrat-Schaden": 0.01,
          "Haftpflicht": 0.02,
          "Kfz-Schaden": 99.97,
          "Reiseschaden": 0.0,
          "Tierkrankheit": 0.0
        }
        ```
    (Note: The example probabilities above are illustrative.)

---

## Key Components/Files

*   `flask_server.py`: The main Flask application file. It defines the `/evaluate-email` API endpoint and handles incoming requests.
*   `prediction.py`: Contains the core logic for loading the pre-trained machine learning model and making predictions on e-mail text.
*   `training/training.py`: Includes scripts and functions related to training the classification model.
*   `training/training_data/`: This directory contains generated e-mails used for fine tuning (e.g., `emails_1.json`, `emails_2.json`).
*   `training/email_generator.py`: A script used for generating synthetic email data for testing or development purposes.
*   `requirements.txt`: Lists all Python dependencies required for this service. These are installed using `pip install -r requirements.txt`.
*   `Dockerfile`: Defines the instructions for building a Docker image for this service, enabling containerized deployment.

---

## Requirements

*   **Python**: Version 3.x (as specified by the development environment, typically 3.7+ for modern ML libraries).
*   **pip**: For installing Python packages.
*   **Python Dependencies**: As listed in `requirements.txt`. Key libraries include:
    *   `Flask`
    *   `transformers`
    *   `torch`
    *   `numpy`
    *   `scipy`
    *   `datasets`
    *   `evaluate`
*   **Docker**: Required if you intend to run the service as a Docker container (Docker Desktop or equivalent).
