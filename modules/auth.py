from flask import request, current_app, jsonify

API_KEY='bla'

def chk_auth():
    current_app.logger.info(f'{request.headers.get("Authorization")}')
    if request.headers.get('Authorization').replace('Bearer', '').strip() != API_KEY:
        return jsonify( {'error':f'Wrong key'} ), 403    


from functools import wraps
from flask import request, current_app, jsonify

API_KEY = "bla"

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        current_app.logger.info(auth_header)

        token = auth_header.replace("Bearer", "").strip()

        if token != API_KEY:
            return jsonify({"error": "Wrong key"}), 403

        return f(*args, **kwargs)

    return decorated