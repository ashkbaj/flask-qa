import datetime

from flask import Flask, abort,jsonify, flash, redirect, url_for, request, render_template
from markupsafe import escape
import json
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
import os, base64;
from sentry_sdk.integrations.flask import FlaskIntegration



#basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/flaskdb'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "aab27cfde51a0cd8"
db = SQLAlchemy(app)



class Student(db.Model):
    id = db.Column('std_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    standard = db.Column(db.String(10))
    city = db.Column(db.String(40))

    def __init__(self, name, std, city):
        self.id = id
        self.standard = std
        self.city = city
        self.name = name





@app.route('/')
def home():
    return "Mic testing ok"

@app.route('/index')
def index():
    return render_template('index.html', utc_time = datetime.datetime.utcnow())

@app.route('/aboutus')
def about():
    return "About testing ok"

@app.route('/escape/<inputstring>/')
def capitalise(inputstring):
    return '<h1>{}</h1>'.format(escape(inputstring.capitalize()))


@app.route('/add/<int:n1>/<int:n2>')
def add(n1, n2):
    return '<h1>{}</h1>'.format(n1+n2)


@app.route('/users/<int:user_id>/')
def greet_user(user_id):
    users = ['Bob', 'Jane', 'Adam']
    try:
        return '<h2>Hi {}</h2>'.format(users[user_id])
    except IndexError:
        abort(404)


@app.route('/users2/<int:user_id>/')
def greet_user2(user_id):
    users = {1: 'Bob', 2: 'Jane', 3: 'Adam'}
    try:
        return '<h2>Hi {}</h2>'.format(users[user_id])
    except IndexError:
        abort(404)


# URL Redirection
@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest


@app.route('/routingurl/<name>')
def routingurl(name):
    print(name)
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))

@app.route('/generatecode')
def generate_secret_code():
    return  base64.b64encode(os.urandom(32))

@app.route('/csvtojson')
def csvtojson():
    return 1

@app.route('/dbtojson')
def dbtojson():


    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="flaskdb"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT id, name, username, pwd FROM tbl_user4")

    myresult = mycursor.fetchall()

    # for x in myresult:
    # print(x)
    #with app.app_context():
        #jsonify(result=myresult)

    #jsonoutput = json.dumps(myresult)
    #print(type(myresult))
    return json.loads(json.dumps(myresult))
    #return f"json: {json.dumps(myresult)}"

@app.route('/success/<name>/<method>')
def success(name, method):
    return '{} - login eligible for {}'.format(method, name)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user, method=request.method))

    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user, method=request.method))


@app.route('/showstudents', methods=['POST','GET'])
def allstudents():
    #students = students.query.all()
    return render_template('showallstudents.html', students=Student.query.all())



@app.route('/addstudent', methods = ['GET','POST'])
def addstudent():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['standard']:
            flash('Please enter all the fields', 'error')
        else:
            print('inside else')
            student = Student(request.form['name'], request.form['city'], request.form['standard'])
            print(student.name)
            db.session.add(student)
            db.session.commit
            flash('Student added successfully')

            return redirect(url_for('allstudents'))
    return render_template('newstudent.html')



if app.name == "__main__":
    app.run()


