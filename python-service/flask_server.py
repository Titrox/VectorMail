from flask import Flask, request, jsonify
import logging
import prediction

# Setting up basic logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()

# Initialize Flask application
app = Flask(__name__)


@app.route('/evaluate-email', methods=['POST'])
def evaluate_email():
    
    email = request.json
    logger.debug(email)
    probabilities = prediction.predict_label(email).squeeze().numpy() * 100


    # NumPy Floats are not json parseble!
    probs = {
        "Kfz-Schaden": float(round(probabilities[0],2)),
        "Hausrat-Schaden": float(round(probabilities[1],2)),
        "Haftpflicht": float(round(probabilities[2],2)),
        "Reiseschaden": float(round(probabilities[3],2)),
        "Tierkrankheit": float(round(probabilities[4],2)),
    }

    return jsonify(probs)

# Run the Flask app if this file is executed directly
if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000, debug=True)