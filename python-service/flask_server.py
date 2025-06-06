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
    
    logger.debug(request.json)

    # Todo
    probs = {
        "Kfz-Schaden": random.uniform(0,100),
        "Hausrat-Schaden": random.uniform(0,100),
        "Haftpflicht": random.uniform(0,100),
        "Reiseschaden": random.uniform(0,100),
        "Tierkrankheit": random.uniform(0,100),
    }


    return jsonify(probs)

# Run the Flask app if this file is executed directly
if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000, debug=True)