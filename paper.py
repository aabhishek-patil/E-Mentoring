from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("admin.html")

@app.route('/marks1',methods=['POST','GET'])
def marks1():
	if request.method == 'POST':
		marks1 = request.form
		return render_template("marks1.html",marks1=marks1)


# @app.route('/query')
# def query():
# 	return render_template("paper.html")

if __name__ == "__main__":
    app.run(debug=True)

