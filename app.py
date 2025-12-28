"""
Happy Number Service using Flask.

This application provides an API to check if a number is a "happy number".
A happy number is a number which eventually reaches 1 when replaced by the sum
of the square of its digits.
"""
import logging
from flask import Flask, jsonify

# Configure structured logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

def is_happy(n):
    """
    Determines if a number is a happy number using a cycle detection algorithm.

    Args:
        n: A positive integer.

    Returns:
        True if the number is happy, False otherwise.
    """
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(digit) ** 2 for digit in str(n))
    return n == 1


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify service is running."""
    return jsonify({"status": "healthy"}), 200


@app.route("/is_happy/<int:number>", methods=["GET"])
def check_happy_number(number):
    """Checks if the provided number is a happy number."""
    if number <= 0:
        return jsonify({"error": "Number must be a positive integer."}), 400

    result = is_happy(number)
    logging.info("Checked number %d, is_happy: %s", number, result)
    return jsonify({"number": number, "is_happy": result}), 200


@app.route("/", methods=["GET"])
def index():
    """Index endpoint providing a welcome message and usage instructions."""
    return jsonify(
        {
            "message": "Welcome to the Happy Number API!",
            "usage": "GET /is_happy/<positive_integer>",
        }
    )


if __name__ == "__main__":
    # This block is for local development and is not used by Gunicorn.
    app.run(host="0.0.0.0", port=5000)
