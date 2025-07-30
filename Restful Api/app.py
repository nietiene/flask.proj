from flask import Flask, request, jsonify
# request lets you access incoming data like form or json
# jsonify convert python data into JSON data
app = Flask(__name__)

# fake database for study

students = {
    1: {"name": "Etiene", "Age": 17},
    2: {"name": "Alice", "Age": 22},
}


# get all studentd
@app.route('/students', methods=['GET'])
def get_students():
    # convert student dictionary data to JSON and return it 
    return jsonify(students)

# get one student by ID
@app.route('/students/<int:student_id>', methods=['GET'])\

def get_student(student_id):
    student = students.get(student_id)
    # students.get fetch student from the dictionary based on his ID
    if student:
        return jsonify(student)
    # return json data
    return jsonify({ "message": "Student not found" }), 404

# POST- add new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    # request.get_json() gets JSON data sent by the user
    new_id = max(students.keys()) + 1
    # creates new ID by taking highest id and adding it to one
    students[new_id] = data
    
    # add new student to the dictionary
    return jsonify({ "message": "Student added", "id": new_id, "student": data}), 201


# PUT - update student
@app.route('/students/<int:student_id>', methods=['PUT'])

def update_student(student_id):
    if student_id in students:
        data = request.get_json()
        students[student_id] = data
        # it replace the old data to the new data
        return jsonify({ "message": "Student updated", "student": data })
    return jsonify({ "message": "Student not found" }), 404 

# DELETE - student
@app.route('/students/<int:student_id>', methods=['DELETE'])

def delete_student(student_id):
    if student_id in students:
        del students[student_id]
        return jsonify({ "message": "Student deleted" })
    return jsonify({ "message": "Student not found" }), 404


if __name__ == "__main__":
    app.run(debug=True)