from flask import jsonify
from typing import Any


def success_response(data: Any = None, message: str = 'Success', status_code: int = 200):
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    }), status_code


def error_response(message: str = 'An error occurred', status_code: int = 400):
    return jsonify({
        'success': False,
        'message': message,
        'data': None
    }), status_code
