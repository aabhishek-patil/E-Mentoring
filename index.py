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
def home():
    return render_template('main.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    if "userloggedin" in session:
        return redirect("/")
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM db.accounts WHERE username = %s AND password = %s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['userloggedin'] = True
            session['uid'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('main.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM db.accounts WHERE username = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO db.accounts VALUES (NULL, %s, %s, %s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/doubt', methods =['GET', 'POST'])
def doubt():
    return render_template('doubt.html')


@app.route('/query1', methods =['GET', 'POST'])
def query1():

    return render_template('query1.html')

@app.route('/query2', methods =['GET', 'POST'])
def query2():
    return render_template('query2.html')

@app.route('/query3', methods =['GET', 'POST'])
def query3():
    return render_template('query3.html')

@app.route('/lec1', methods =['GET', 'POST'])
def lec1():
    cursor = mysql.connection.cursor()
    que = "SELECT * FROM db.videos"
    cursor.execute(que)
    val = cursor.fetchall()
    print(val)
    return render_template('lec1.html',val=val)

@app.route('/lec2', methods =['GET', 'POST'])
def lec2():
    cursor = mysql.connection.cursor()
    que = "SELECT * FROM db.videos2"
    cursor.execute(que)
    val = cursor.fetchall()
    print(val)
    return render_template('lec2.html',val=val)

@app.route('/lec3', methods =['GET', 'POST'])
def lec3():
    cursor = mysql.connection.cursor()
    que = "SELECT * FROM db.videos3"
    cursor.execute(que)
    val = cursor.fetchall()
    print(val)
    return render_template('lec3.html',val=val)


@app.route('/feedback', methods =['GET', 'POST'])
def feedback():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        feedback = request.form['feedback']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO db.feedback VALUES (NULL,%s, %s)', (email, feedback))
        mysql.connection.commit()
        return render_template("feedback.html")

    else:
        return render_template('feedback.html')

@app.route('/profile/<int:no>', methods =['GET', 'POST'])
def profile(no):
    id1 = no
    print(id1)
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM db.accounts WHERE id like '{}' """.format(id1))
    looks=cursor.fetchall()
    print(looks)
    return render_template('profile.html',looks=looks)


##################################################################

@app.route('/mhome', methods =['GET', 'POST'])
def mhome():
    return render_template('mmain.html')


@app.route('/mlogin', methods =['GET', 'POST'])
def mlogin():
    if "mentorloggedin" in session:
        return redirect("/mhome")
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM db.mentor WHERE username = %s AND password = %s', (username, password, ))
        account = cursor.fetchone()
        print(account)
        if account:
            session['mentorloggedin'] = True
            session['mentorid'] = account[0]
            session['mentorusername'] = account[1]
            msg = 'Logged in successfully !'
            print(msg)
            return render_template('mmain.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('mlogin.html', msg = msg)

# @app.route('/mlogout')
# def mlogout():
#     session.pop('mentorloggedin', None)
#     session.pop('mentorid', None)
#     session.pop('mentorusername', None)
#     return redirect(url_for('mlogin'))


@app.route('/mregister', methods =['GET', 'POST'])
def mregister():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM db.mentor WHERE username = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO db.mentor VALUES (NULL, %s, %s, %s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('mregister.html', msg = msg)




@app.route('/query', methods =['GET', 'POST'])
def query():
    msg = ''
    if request.method == 'POST':
        uid = session['uid'] 
        # uid = 3
        questionid = random.randint(0000,9999)
        mentor = request.form['mentor'].strip()
        question = request.form['question'].strip()
        subject = request.form['subject'].strip()
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO db.user_question(questionid,userid,subject,mentorname,question,status) VALUES (%s, %s, %s, %s,%s,%s)', (questionid,uid,subject,mentor, question, 0, ))
        mysql.connection.commit()
        msg="Question Sent"
    return render_template('query.html')

@app.route('/mentor_solve', methods =['GET', 'POST'])
def mentor_solve():
    if "mentorloggedin" not in session:
        return redirect("/mlogin")
    msg = ''
    userquestion=None
    cursor = mysql.connection.cursor()
    a=session['mentorusername']
    print(a)
    # a = "Mentor1"
    cursor.execute('SELECT * FROM db.user_question WHERE mentorname = %s and status = %s', (a,0,))
    userquestion = cursor.fetchone()
    print(userquestion)
    if request.method == 'POST':
        answer = request.form['mentoranswer'].strip()
        questionid = request.form['questionid'].strip()
        userid = request.form['userid'].strip()
        cursor = mysql.connection.cursor()
        cursor.execute('insert into db.mentorans values(%s,%s,%s)',(questionid,answer,userid,))
        mysql.connection.commit()
        cursor.execute('update db.user_question set status=1 where questionid=%s',(questionid,))
        mysql.connection.commit()
        print("Answer updated")  
        msg="Answer Updated"
        cursor.execute('SELECT * FROM db.user_question WHERE mentorname = %s and status = %s', (a,0,))
        userquestion = cursor.fetchone()
    if userquestion==None:
        msg="No new questions for you:("
    return render_template('mentor_solve.html',userquestion=userquestion,msg=msg)

# @app.route('/solve', methods =['GET', 'POST'])
# def solve():
#     cursor = mysql.connection.cursor()
#     # query='SELECT * FROM db.mentorans,db.user_question WHERE userid=%s'
#     query="SELECT u.*,p.* FROM db.mentorans u JOIN db.user_question p ON u.questionid=p.questionid  WHERE u.userid=%s"
#      # cursor.execute(query,(session['uid'],))
#     cursor.execute(query,(3,))
#     data=cursor.fetchall()
#     cursor.close()
#     print(data)
#     return render_template("solve.html", mentorans=data)

@app.route('/solveform',methods = ['POST','GET'])
def solveform():
    return render_template('solveform.html')

@app.route('/solve', methods = ['POST','GET'])
def solve():
    if request.method == "POST":
        uid = request.form.get("userid")
    cursor = mysql.connection.cursor()
    query="SELECT u.*,p.* FROM db.mentorans u JOIN db.user_question p ON u.questionid=p.questionid  WHERE u.userid=%s"
    cursor.execute(query,(uid,))
    data = cursor.fetchall()
    cursor.close()
    return render_template('solve.html',mentorans=data)

############admin####

@app.route('/adminlog')
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
def feedback1():
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


@app.route('/alec1', methods =['POST', 'GET'])
def lecc():
    print("yesssss")
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


@app.route('/lec2', methods =['POST', 'GET'])
def lecc2():
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


@app.route('/alec3', methods =['POST', 'GET'])
def lecc3():
    cursor = mysql.connection.cursor()
    que = "SELECT * FROM db.videos3"
    cursor.execute(que)
    val = cursor.fetchall()
    print(val)
    return render_template('addcourse3.html',val=val)


# @app.route('/lec3', methods =['GET', 'POST'])
# def lec3():
#     cursor = mysql.connection.cursor()
#     que = "SELECT * FROM db.videos3"
#     cursor.execute(que)
#     val = cursor.fetchall()
#     print(val)
#     return render_template('lec3.html',val=val)




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

