from flask import Blueprint, request, jsonify, render_template
from modules.functions import semantic_search

api = Blueprint('api', __name__)

@api.route("/")
def welcome():
    return render_template('welcome.html')

@api.route("/semantic-search", methods=['POST'])
def search():
    try:
        data = request.get_json()
        result = semantic_search(data)
        response = jsonify(result)
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"error": str(e)})
        response.status_code = 500
        return response