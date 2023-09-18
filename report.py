from flask import Flask,request, redirect, url_for, flash,render_template
from flask_mysqldb import MySQL

from fpdf import FPDF
from datetime import datetime
date = datetime.now()
from flask import Flask, Response, render_template
app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db'

mysql = MySQL(app)

@app.route('/')
def upload_form():
    return render_template('download.html')

@app.route('/download/report/pdf')
def download_report():
    now = date.today()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user_question")
    result = cursor.fetchall()
    
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.set_font('Times','B',10.0)
    pdf.cell(page_width,0.0,"Question Report",align = "C")
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,'Date:- '+str(date.strftime("%d / %m / %y")),align="L")
    pdf.ln(10)
    pdf.set_font('Courier','',7.0)
    col_width = page_width/2
    pdf.ln(1)
    th = pdf.font_size
    i = 1
    # pdf.cell(col_width*1,th,"Sr.no",border=1)
    # pdf.cell(col_width*1,th,"userid",border=1)
    # pdf.cell(col_width*2,th,"username",border=1)
    # pdf.cell(col_width*3s,th,"email",border=1)
    pdf.cell(col_width+70,th,"questions",border=1)
    # pdf.cell(col_width,th,"mentoranswer",border=1)
    pdf.ln(th)
    print(result)
    for row in result:
        # pdf.cell(col_width*1,th, str(i),border=1)
        # pdf.cell(col_width*1,th, str(row[0]),border=1)
        # pdf.cell(col_width*2,th,str(row[1]),border=1)
        # pdf.cell(col_width*3,th, row[3],border=1)
        # pdf.cell(col_width,th, row[1],border=1)
        # pdf.cell(col_width*8,th, row[1].encode('utf-8').decode('latin-1'),border=1)
        pdf.multi_cell(col_width+70,th, row[4].encode('utf-8').decode('latin-1'),border=1)
        i=i+1
        pdf.ln(th)
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    cursor.execute('SELECT COUNT(Question) FROM db.user_question')
    count=cursor.fetchone()
    count1=str(count[0])
    print(count)
    pdf.cell(page_width,0.0,"Total count ="+count1,align='L')
    pdf.ln(10)
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width,0.0,'-end of report-',align='C')
    return Response(pdf.output(dest='s').encode('latin-1'),mimetype='application/pdf',headers={'Content-Disposition':'attachment;filename=student_report.pdf'})

if __name__ == "__main__":
    app.run(debug=True)