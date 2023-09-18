from flask import Flask , render_template
app=Flask(__name__)

@app.route("/<int:no>")
def index(no):
	return render_template("j2.html",n=no)