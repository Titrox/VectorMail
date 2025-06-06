from flask import Flask, request
import logging
import random
from flask import jsonify

# Setting up basic logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()

# Initialize Flask application
app = Flask(__name__)


@app.route('/evaluate-email', methods=['POST'])
def evaluate_email():
    
    # Todo
    probs = {
        "Schadensmeldung": random.randint(0,100),
        "Vertragsänderung": random.randint(0,100),
        "Rückfragen": random.randint(0,100),
        "Bewerbung": random.randint(0,100),
        "Kündigung": random.randint(0,100),
        "Spam": random.randint(0,100),
        "Sonstiges": random.randint(0,100),
    }

    return jsonify(probs)

# Run the Flask app if this file is executed directly
if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000, debug=True)