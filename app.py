from flask import Flask, request, jsonify
from opensearchpy import OpenSearch

app = Flask(__name__)

# OpenSearch client configuration
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "Opensearch#2025"),
    use_ssl=True,
    verify_certs=False
)

INDEX_NAME = "student_records"

# POST: Add a student
@app.route('/student', methods=['POST'])
def add_student():
    data = request.json
    student_id = data.get("student_id")
    response = client.index(index=INDEX_NAME, id=student_id, body=data)
    return jsonify({"message": "Student added", "result": response['result']}), 201

# GET: Get student by ID
@app.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    try:
        result = client.get(index=INDEX_NAME, id=student_id)
        return jsonify(result['_source'])
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# DELETE: Delete student by ID
@app.route('/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        response = client.delete(index=INDEX_NAME, id=student_id)
        return jsonify({"message": "Student deleted", "result": response['result']})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
