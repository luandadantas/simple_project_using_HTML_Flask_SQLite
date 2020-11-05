import sqlite3
from flask import Flask, render_template, request
app = Flask(__name__)

connection = sqlite3.connect('database.db')
# print("Database connection successfully")

# connection.execute('CREATE TABLE participants (name TEXT, age INTEGER, city TEXT)')
# print("Table created successfully")

# connection.close()

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_participant():
    return render_template('partcipants.html')

@app.route('/add_record', methods = ['POST', 'GET'])
def add_record():
    if request.method == 'POST':
        try:
            name = request.form['name']
            age = request.form['age']
            city = request.form['city']

            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()

                cursor.execute("INSERT INTO participants (name, age, city) VALUES (?,?,?)", (name, age, city))
                connection.commit()
                msg = "Record successfully added"       
        except:
            connection.rollback()
            msg = "error in insert operation"
        
        finally:
            return render_template("result.html", msg = msg)
            connection.close()

@app.route("/list")
def list():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("select * from participants")

    rows = cursor.fetchall()
    return render_template("list.html", rows = rows)

if __name__ == '__main__':
    app.run(debug= True)
