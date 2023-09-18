from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
# import MySQLdb.cursors
import re
import random


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db'

mysql = MySQL(app)

@app.route('/')
def adminlog():
    return render_template('admin.html')

@app.route('/alogin', methods =['GET', 'POST'])
def alogin():
    if "adminloggedin" in session:
        return redirect("/")
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM db.admin WHERE username = %s AND password = %s', (username, password, ))
        account = cursor.fetchone()
        print(account)
        if account:
            session['adminloggedin'] = True
            session['adminid'] = account[0]
            session['adminusername'] = account[3]
            msg = 'Logged in successfully !'
            print(msg)
            return render_template('admin.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('alogin.html', msg = msg)

@app.route('/usertable', methods = ['POST','GET'])
def usertable():
    cursor = mysql.connection.cursor()
    query='SELECT * FROM accounts,user_question,mentorans WHERE accounts.id = user_question.userid'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('usertable.html',vals =data)

@app.route('/feedback', methods = ['POST','GET'])
def feedback():
    cursor = mysql.connection.cursor()
    query='SELECT * FROM db.feedback'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('feed.html',feedback=data)

@app.route('/mento', methods = ['POST','GET'])
def mento():
    cursor = mysql.connection.cursor()
    query='SELECT * FROM db.mentor'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('mento.html',mentor=data)

@app.route('/selectlec', methods = ['POST','GET'])
def selectlec():
    return render_template('selectlec.html')

# @app.route('/query', methods = ['POST','GET'])
# def query():
#     cursor = mysql.connection.cursor()
#     que = "SELECT * FROM db.subject"
#     cursor.execute(que)
#     val = cursor.fetchall()
#     print(val)
#     return render_template('selectlec.html',val=val)


# @app.route('/delsub/<int:no>', methods =['GET', 'POST'])
# def delsub(no):
#     cursor = mysql.connection.cursor()
#     que = ("DELETE  FROM db.subject WHERE no = {}".format(no))
#     cursor.execute(que)
#     mysql.connection.commit()
#     print("abhi")
#     return redirect('/query')

# @app.route('/addsub', methods =['GET', 'POST'])
# def addsub():
#     if request.method == 'POST':
#         name = request.form['name']
#         anchor = request.form['anchor']
#         cursor = mysql.connection.cursor()
#         que = "INSERT INTO db.subject(no,name,anchor) VALUES(NULL,%s,%s)"
#         val = (name,anchor)
#         cursor.execute(que,val)
#         mysql.connection.commit()
#         return redirect('/query')

############################################

@app.route('/lec1', methods =['POST', 'GET'])
def lec1():
    print("yesssssssssssssssssssssssssssssssssssssssssssss")
    cursor = mysql.connection.cursor()
    que = "SELECT * FROM db.videos"
    cursor.execute(que)
    val = cursor.fetchall()
    print(val)
    return render_template('addcourse.html',val=val)


@app.route('/dellec/<int:no>', methods =['GET', 'POST'])
def dellec(no):
    cursor = mysql.connection.cursor()
    que = ("DELETE  FROM db.videos WHERE no = {}".format(no))
    cursor.execute(que)
    mysql.connection.commit()
    print("abhi")
    return redirect('/lec1')

@app.route('/addlec', methods =['GET', 'POST'])
def addlec():
    if request.method == 'POST':
        name = request.form['name']
        path = request.form['path']
        cursor = mysql.connection.cursor()
        que = "INSERT INTO db.videos(name, path, no) VALUES(%s,%s,NULL)"
        val = (name,path)
        cursor.execute(que,val)
        mysql.connection.commit()
        return redirect('/lec1')

############lec2############

@app.route('/lec2', methods =['POST', 'GET'])
def lec2():
    cursor = mysql.connection.cursor()
    que = "SELECT * FROM db.videos2"
    cursor.execute(que)
    val = cursor.fetchall()
    print(val)
    return render_template('addcourse2.html',val=val)


@app.route('/dellec2/<int:no>', methods =['GET', 'POST'])
def dellec2(no):
    cursor = mysql.connection.cursor()
    que = ("DELETE  FROM db.videos2 WHERE no = {}".format(no))
    cursor.execute(que)
    mysql.connection.commit()
    print("abhi")
    return redirect('/lec2')

@app.route('/addlec2', methods =['GET', 'POST'])
def addlec2():
    if request.method == 'POST':
        name = request.form['name']
        path = request.form['path']
        cursor = mysql.connection.cursor()
        que = "INSERT INTO db.videos2(name, path, no) VALUES(%s,%s,NULL)"
        val = (name,path)
        cursor.execute(que,val)
        mysql.connection.commit()
        return redirect('/lec2')

#################lec3################

@app.route('/lec3', methods =['POST', 'GET'])
def lec3():
    cursor = mysql.connection.cursor()
    que = "SELECT * FROM db.videos3"
    cursor.execute(que)
    val = cursor.fetchall()
    print(val)
    return render_template('addcourse3.html',val=val)


@app.route('/dellec3/<int:no>', methods =['GET', 'POST'])
def dellec3(no):
    cursor = mysql.connection.cursor()
    que = ("DELETE  FROM db.videos3 WHERE no = {}".format(no))
    cursor.execute(que)
    mysql.connection.commit()
    print("abhi")
    return redirect('/lec3')

@app.route('/addlec3', methods =['GET', 'POST'])
def addlec3():
    if request.method == 'POST':
        name = request.form['name']
        path = request.form['path']
        cursor = mysql.connection.cursor()
        que = "INSERT INTO db.videos3(name, path, no) VALUES(%s,%s,NULL)"
        val = (name,path)
        cursor.execute(que,val)
        mysql.connection.commit()
        return redirect('/lec3')


if __name__ == "__main__":
    app.run(debug=True)