from flask import jsonify
from app import app

# Handle 404 error
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

# Handle 500 error
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Handle rate limit error
@app.errorhandler(429)
def rate_limit_error(error):
    return jsonify({'error': 'Rate limit exceeded, please try again later'}), 429

# Handle bad request error
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad request'}), 400

# Custom error handling can be extended here