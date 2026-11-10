from flask import Blueprint, request, current_app, jsonify
import json
import re
import os
from modules.auth import require_api_key

app = Blueprint('api', __name__)

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.json')
SCORES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scores.json')

def read_data():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def write_data(data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def read_scores():
    try:
        with open(SCORES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def write_scores(data):
    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(read_data())

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    users = read_data()
    for user in users:
        if user['id'] == id:
            return jsonify(user)
    return jsonify({'error': f'User {id} not found'}), 404

@app.route('/user/<input>', methods=['GET'])
def get_user_by_emailor_name(input):
    email_pattern = re.compile(r"^[\w.-]+@[\w.-]+\.\w+$")
    users = read_data()
    for user in users:
        matches = email_pattern.findall(input)
        if matches and matches[0] == input:
            if user['email'] == input:
                return jsonify(user)
        else:
            if user['name'] == input:
                return jsonify(user)
    return jsonify({'error': f'User "{input}" not found'}), 404

@app.route('/user', methods=['POST'])
@require_api_key
def add_new_user():
    data = request.get_json()
    if not data or 'email' not in data or 'name' not in data:
        return jsonify({'error': 'Not all fields have been submitted'}), 400
    users = read_data()
    for user in users:
        if user['name'] == data['name'] and user['email'] == data['email']:
            return jsonify({'error': 'User already exists'}), 400
    new_id = max((u['id'] for u in users), default=0) + 1
    new_user = {
        'id': new_id,
        'name': data['name'],
        'email': data['email'],
        'age': data.get('age')
    }
    users.append(new_user)
    write_data(users)
    return jsonify(new_user)

@app.route('/user/<int:id>', methods=['DELETE'])
@require_api_key
def remove_user_by_id(id):
    users = read_data()
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        return jsonify({'error': f'User {id} not found'}), 404
    users = [u for u in users if u['id'] != id]
    write_data(users)
    return jsonify({'message': f'User {id} deleted'})

# --- VR TARGET SHOOTER ENDPOINTS ---

@app.route('/scores', methods=['GET'])
def get_vr_scores():
    scores = read_scores()
    sorted_scores = sorted(scores, key=lambda x: x.get('score', 0), reverse=True)[:10]
    return jsonify(sorted_scores)

@app.route('/scores', methods=['POST'])
def add_vr_score():
    data = request.get_json()
    if not data or 'score' not in data:
        return jsonify({'error': 'Missing score'}), 400
    scores = read_scores()
    new_id = max((s.get('id', 0) for s in scores), default=0) + 1
    entry = {
        'id': new_id,
        'player': str(data.get('player', 'VR_Player'))[:20],
        'score': int(data.get('score', 0)),
        'accuracy': str(data.get('accuracy', '100%')),
        'mode': str(data.get('mode', 'Reflex'))
    }
    scores.append(entry)
    write_scores(scores)
    sorted_scores = sorted(scores, key=lambda x: x.get('score', 0), reverse=True)[:10]
    return jsonify({'message': 'Score saved', 'entry': entry, 'leaderboard': sorted_scores}), 201
