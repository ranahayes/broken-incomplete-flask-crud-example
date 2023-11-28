from flask import Flask
from flask import request
from flask import render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'secret'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = '34.125.223.69'
mysql.init_app(app)

@app.route("/add") #Add Student
def add():
  name = request.args.get('name')
  email = request.args.get('email')
  try:
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email) # kludge - use stored proc or params
    cur.execute(s)
    mysql.connection.commit()

    return '{"Result":"Success"}'
  except Exception as e:
    return '{"Result":"Failure", "Error":"' + str(e) + '"}'
@app.route("/") #Default - Show Data
def read(): # Name of the method
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return render_template('index.html',results=Results) #render index.html with Results

@app.route("/delete") #Add Student
def delete():
  id = request.args.get('id')
  try:
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    s='''DELETE FROM students WHERE studentID = '{}';'''.format(id) # kludge - use stored proc or params
    cur.execute(s)
    mysql.connection.commit()

    return '{"Result":"Success"}'
  except Exception as e:
    return '{"Result":"Failure", "Error":"' + str(e) + '"}'
  
@app.route("/update") #Add Student
def update():
  id = request.args.get('id')
  name = request.args.get('name')
  email = request.args.get('email')
  try:
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    s='''UPDATE students SET studentName = '{}', email = '{}' WHERE studentID = '{}' ;'''.format(name,email,id) # kludge - use stored proc or params
    cur.execute(s)
    mysql.connection.commit()

    return '{"Result":"Success"}'
  except Exception as e:
    return '{"Result":"Failure", "Error":"' + str(e) + '"}'

if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080
