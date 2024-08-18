import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            abort(404, description="Member not found")
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ("first_name", "age", "lucky_numbers")):
            abort(400, description="Missing fields in member data")
        
        jackson_family.add_member(data)
        return jsonify(data), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        if jackson_family.delete_member(member_id):
            return jsonify({"done": True}), 200
        else:
            abort(404, description="Member not found")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
