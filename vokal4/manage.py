from flask_sqlalchemy import SQLAlchemy
from database import Vokabel, Quelle, create
from index import db


def connect():
	connect = create()
	
def grab():
	word = Quelle.query.all()
	coun = count(word)
	return word, coun

def count(que):
	id_co = {}
	for qu in que:
		amount = Vokabel.query.filter_by(quelle_id=qu.id).count()
		id_co[qu.id] = amount
	return id_co


def fetch(qu):
	quelle = Quelle.query.filter_by(id=qu).first()
	table = Vokabel.query.filter_by(quelle_id=qu).all()
	return table, quelle

def find(word):
	result = Vokabel.query.filter(Vokabel.wort.contains(word)).all()
	if not result:
		full, begin, end, conatin="0","0","0","0"
		quellen = "0"
	else:
		quellen = []
		for q in result:
			qu = Quelle.query.filter_by(id=q.quelle_id).first()
			if qu not in quellen:
				quellen.append(qu)
		full,begin,end,conatin = [], [], [], []
		for w in result:
			if w.wort == word:
				full.append(w)
			elif w.wort.startswith(word):
				begin.append(w)
			elif w.wort.endswith(word):
				end.append(w)
			else:
				conatin.append(w)

	return full, begin, end, conatin, quellen

def delete(word):
	target = Vokabel.query.filter_by(id=word).first()
	db.session.delete(target)
	db.session.commit()
	return

def new_qu(title):
	exist = Quelle.query.filter_by(title=title).first()
	if exist:
		return 0
	else:
		new = Quelle(title=title)
		db.session.add(new)
		db.session.commit()
		return 1

def new_pack(wort,bedeu,beis,quel):
	exist = Quelle.query.filter_by(title=quel).first()
	tmp = "null"
	if exist:
		qu_id = exist.id
		c = Vokabel(wort=wort,bedeutung=bedeu,beispiel=beis,quelle_id=qu_id)
		db.session.add(c)
		tmp = qu_id
	else:
		qus = Quelle(title=quel)
		c = Vokabel(wort=wort,bedeutung=bedeu,beispiel=beis)
		qus.Vokabel.append(c)
		db.session.add(qus)
	db.session.commit()
	if tmp=="null":
		tmp = qus.id
	return tmp


