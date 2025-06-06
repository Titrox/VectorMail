from flask import Flask, request
import logging
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
        "Schadensmeldung": 10,
        "Vertragsänderung": 40.2122,
        "Rückfragen": 5,
        "Bewerbung": 10,
        "Kündigung": 10,
        "Spam": 10,
        "Sonstiges": 0,
    }

    return jsonify(probs)

# Run the Flask app if this file is executed directly
if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000, debug=True)