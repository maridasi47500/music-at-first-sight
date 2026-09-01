from flask import Flask, render_template, request, session, redirect
from myplace import Myplace
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_scene", methods=["GET","POST"])
def add_one_scene():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into scene (lieu,lat,lon,profil_qui_parle,ce_qu_on_poste,ouvert_ou_ferme) values (:lieu,:lat,:lon,:profil_qui_parle,:ce_qu_on_poste,:ouvert_ou_ferme)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from scene')


        return render_template("sceneform.html", scenes=user, one_user=one_user, the_title="add new scene")


    user = query_db('select * from scene')
    one_user = query_db("select * from scene limit 1", one=True)
    return render_template("sceneform.html", scenes=user, one_user=one_user, the_title="add new scene")



@app.route("/searchjobcity", methods=["POST"])
def trouver_lieu_city():
    leslieu=Myplace(request.form["lieu"]).trouver1()

    return dict({"city":leslieu[0], "code":leslieu[1], "region":leslieu[3], "departement":leslieu[2], "pays":leslieu[2], "latitude":leslieu[4], "longitude":leslieu[5]})
