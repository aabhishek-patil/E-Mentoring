from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def student():
	return render_template("j1.html")

@app.route('/j2',methods=['POST','GET'])
def home():
	if request.method=="POST"
	j2=request.form
	return render_template('j2.html',j2=j2)
