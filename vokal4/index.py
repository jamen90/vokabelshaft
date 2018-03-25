# -*- coding: utf-8 -*-
from flask import Flask, session, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
import manage
import os
import sys
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbase/deutsch1.db'
db = SQLAlchemy(app)

def init_db():
    manage.connect()
    return

@app.route("/", methods=['POST', 'GET'])
def load():
    init_db()
    if request.method!="POST":
        result=[None,None,None,None,None]
    else:
        word = request.form['word']
        result = manage.find(word)
        #for i in range(0,4):
         #   if len(result[i]) == 0:
          #      result[i]=None
    datas = manage.grab()
    data = datas[0]
    co = datas[1]
    return render_template("home.html", data=data, co=co, fwords=result[0],bwords=result[1],\
                                        ewords=result[2],cwords=result[3], res=result[4])

@app.route("/quelle")
def quelle():
    src = request.args.get('welche')
    table = manage.fetch(src)
    return render_template("table.html", table=table[0], que=table[1])

@app.route("/new_quelle", methods=['POST'])
def new():
    title = request.form['quellen']
    create = manage.new_qu(title)
    if create == 0:
        flash("the title already exists") 
    return redirect(url_for("load"))

@app.route("/add", methods=['POST'])
def add():
    word = request.form['wort']
    mean = request.form['bedeutung']
    examp = request.form['beispiel']
    src = request.form['quelle']
    qu_id = manage.new_pack(word,mean,examp,src)
    table = manage.fetch(qu_id)
    return render_template("table.html", table=table[0], que=table[1])

@app.route("/delete", methods=['POST'])
def delete():
    word = request.form.get('welche')
    back = request.form.get('wo')
    manage.delete(word)
    return redirect(url_for('quelle', welche=back))

#PDF Class...
#https://stackoverflow.com/questions/35608938/converting-html-to-pdf-using-python-flask#35609445
class Pdf():

    def render_pdf(self, name, html):

        from xhtml2pdf import pisa
        from io import BytesIO

        pdf = BytesIO()

        pisa.CreatePDF(BytesIO(html.encode()), pdf)

        return pdf.getvalue()

@app.route('/download', methods=['GET'])
def download():
    src = request.args.get('welche')
    table = manage.fetch(src)
    html = render_template("pdf_table.html", table=table[0], que=table[1], date=datetime.datetime.now().strftime("%d-%m-%y:::%H:%M"))
    file_class = Pdf()
    pdf = file_class.render_pdf('vokabeln', html)
    headers = {
        'content-type': 'application.pdf',
        'content-disposition': 'attachment; filename=vokabeln.pdf'}
    return pdf, 200, headers




if __name__ == "__main__":
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)