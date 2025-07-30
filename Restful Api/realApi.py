from flask import Flask, jsonify, request
# Flask heart of your web app it create flask app project
import pymysql
# pymysql it is library which helps you to creates your flask app

app = Flask(__name__)

# database connection

def get_connection():
    return pymysql.connect(
        # .connect() it creates and returns connection to the MySQL database
        host='localhost',
        user='root',
        password='',
        db='student_api_py',
        cursorclass=pymysql.cursors.DictCursor
        # this tells python to return that as dictionary not turples to make it easily used by jsonify
        # {'id':1, 'name':'etiene'} instead of (1, 'etiene')
    )

# Get all students in database
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_connection()
    # store our connection to conn variable now we are using conn as our  connection
    cursor = conn.cursor()
    # conn.cursor create cursor object which is used to run SQL queries
    # cursor it act like temporary SQL terminal inside python
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    # .fetchall() get all result returned from the query
    conn.close()
    return jsonify(rows)


# get one student by ID
app.route('/students/<int:student_id', methods=['GET'])
def get_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=%s", (student_id,))
    # %s is help to insert save value to avoid XSS attacks
    row = cursor.fetchall()
    conn.close()
    if row:
        return jsonify(row)
    return jsonify({ "message": "Student not found" }), 404


# POST - create a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data['name']
    age = data['age']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age) VALUES(%s, %s)", (name, age))
    conn.commit()
    student_id = cursor.lastrowid
    # lastrowid it gives you an ID of primary key of the new added student
    conn.close()
    return jsonify({ "id": student_id , "name": name, "age": age}), 201


# PUT - update student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    name = data['name']
    age = data['age']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=%s, age=%s WHERE id = %s", (name, age, student_id))
    conn.commit()
    conn.close()
    return jsonify({ "messatge": "Student updated" })   

# DELETE - delete student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def  delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id))
    conn.commit()
    conn.close()
    return jsonify({ "message": "Student deleted" })

if __name__ == "__main__":
    app.run(debug=True)