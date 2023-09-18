from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL 
import re

app=Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='password'
app.config['MYSQL_DB']='project'

mysql=MySQL(app)

@app.route('/')
@app.route('/form', methods =['GET', 'POST'])
def form():
	msg = ''
	if request.method == 'POST' and 'emp_no' in request.form and 'emp_name' in request.form and 'department' in request.form and 'designation' in request.form and'email' in request.form and 'phone_no' in request.form  :
		emp_no = request.form['emp_no']
		emp_name =request.form['emp_name']
		department =request.form['department']
		designation =request.form['designation']
		email = request.form['email']
		phone_no = request.form['phone_no']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM project.employee WHERE email = %s', (email, ))
		data = cursor.fetchone()
		if data:
			msg = 'Account already exists !'
		elif not re.match(r'[A-Za-z]+', emp_name):
			msg = 'Employee name must contain only characters !'

		elif not re.match(r'[0-9]+',phone_no):
			msg = 'phone number must contain only  numbers !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'


		elif not emp_no or not emp_name or not department  or not designation or not email or not phone_no :
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO project.employee  VALUES ( %s , %s, %s, %s, %s, %s)', (emp_no, emp_name, department, designation, email, phone_no,  ))
			mysql.connection.commit()
			session['emp_no'] = request.form['emp_no']

			return redirect (url_for('form2'))
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template("empform.html", msg=msg)


@app.route('/form2', methods =['GET', 'POST'])
def form2():
	msg = ''
	if request.method == 'POST' and 'emp_no' in request.form and 'basic_salary' in request.form and 'grade' in request.form  :
		emp_no = request.form['emp_no']
		basic_salary =request.form['basic_salary']
		grade =request.form['grade']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM project.employee WHERE emp_no = %s', (emp_no, ))
		data = cursor.fetchone()
		if data:

			if not re.match(r'[0-9]+',emp_no):
				msg = 'Employee number contain only  numbers !'
			elif not re.match(r'[0-9]+',basic_salary):
				msg = 'Basic Salary contain only  numbers !'
			elif not re.match(r'[A-D]+',grade):
				msg = 'grade contain only A B C D !'

			elif not emp_no or not basic_salary or not grade  :
				msg = 'Please fill out the form !'
			else:
				cursor.execute('INSERT INTO project.payment  VALUES ( %s , %s, %s)', (emp_no, basic_salary, grade,   ))
				mysql.connection.commit()
				return redirect (url_for('option'))
		else:
			msg = 'Employee does not exists.'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template("empform2.html", msg=msg)


@app.route('/option', methods =['GET', 'POST'])
def option():
	return render_template("option.html")

@app.route('/individual')
def individual():
	emp_no=session.get('emp_no')
	print(emp_no)
	cursor = mysql.connection.cursor()
	query = 'SELECT * FROM project.employee,project.payment WHERE employee.emp_no=%s AND payment.emp_no=%s'
	cursor.execute(query,(emp_no,emp_no, ))
	data = cursor.fetchall()
	cursor.close()
	return render_template("individual.html", d = data)

@app.route('/summary')
def summary():
	cursor = mysql.connection.cursor()
	query = 'SELECT * FROM project.employee,project.payment WHERE employee.emp_no=payment.emp_no'
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	return render_template("summary.html", e = data)

if __name__ == "__main__":
    app.run()
