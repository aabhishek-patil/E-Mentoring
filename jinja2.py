from flask import Flask , renter_template
app=Flask(__name__)

@app.route("/<int:no>")
def index(no):
	return renter_template(j2.html,n=no)