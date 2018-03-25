# -*- coding: utf-8 -*-
from flask import Flask, session, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
import manage
import os
import sys


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
        result=[None,None]
    else:
        word = request.form['word']
        result = manage.find(word)
    datas = manage.grab()
    data = datas[0]
    co = datas[1]
    return render_template("home.html", data=data, co=co, words=result[0], res=result[1])

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

@app.route("/delete")
def delete():
    word = request.args.get('welche')
    back = request.args.get('wo')
    manage.delete(word)
    return redirect(url_for('quelle', welche=back))

@app.route('/download')
def download():
    src = request.args.get('welche')
    table = manage.fetch(src)
    data = table[0]
    gene(data)
    return redirect(url_for('load'))

def gene(data):
    with open('vaokabeln.txt','a',encoding="UTF-8") as file:
        for datum in data:
            file.write("{0} : {1} : {2} \n".format(datum.wort,datum.bedeutung,datum.beispiel))
    return



if __name__ == "__main__":
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)