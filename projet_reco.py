#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import sys
from flask import Flask, redirect,url_for , send_from_directory, render_template, request, flash
from flask import render_template
from werkzeug.utils import secure_filename
import urllib
import sqlite3
from pylti.flask import lti
import MySQLdb
from get_params import get_params
import xlrd

VERSION = '0.0.5'
UPLOAD_FOLDER='exos/'
ALLOWED_EXTENSIONS=set(['xlsx'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config.from_object('config')





def error(exception=None):
    """ Page d'erreur """
    return render_template('error.html')


@app.route('/is_up', methods=['GET'])
def hello_world(lti=lti):
    """ Test pour debug de l'application

    :param lti: the `lti` object from `pylti`
    :return: simple page that indicates the request was processed by the lti
        provider
    """
    return render_template('up.html', lti=lti)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/lti/', methods=['GET', 'POST'])
@lti(request='initial', error=error, app=app)
def index(lti=lti):
    """ Page d'acceuil, permet d'authentifier l'utilisateur.

    :param lti: the `lti` object from `pylti`
    :return: index page for lti provider
    """
    return render_template('index.html', lti=lti)


@app.route('/index_staff', methods=['GET', 'POST'])
@lti(request='session', error=error, role='staff', app=app)
def index_staff(lti=lti):
    """ Affiche le template staff.html

    :param lti: the `lti` object from `pylti`
    :return: the staff.html template rendered
    """
    return render_template('staff.html', lti=lti)

#Permet de restrindre les uploads à un format excel
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/upload_exo', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def upload_exo(lti=lti):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser will
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            file.name='bdd_exos'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'bdd.xlsx'))
            return redirect(url_for('majDB'))
        if file and not allowed_file(file.filename):
            flash('Mauvais format, les formats possibles sont : ' + str(ALLOWED_EXTENSIONS).split('set([')[-1].split('])')[0])
    return render_template('testupload.html', lti=lti)
    
@app.route('/maj_db', methods=['GET','POST'])
@lti(request='session', error=error, role='staff', app=app)
def majDB(lti=lti):
    database = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = database.cursor() 
    cHandler.execute("DELETE FROM mdl_exos_recommendation")
    cHandler.execute("CREATE TABLE IF NOT EXISTS mdl_exos_recommendation (num_exo integer, theme integer, savoir_faire integer)")
    # Open the workbook and define the worksheet
    book = xlrd.open_workbook("./exos/bdd.xlsx")
    sheets=book.sheet_names()
    sheet1 = book.sheet_by_name(sheets[1])
    sheet2 = book.sheet_by_name(sheets[2])
    # Get the cursor, which is used to traverse the database, line by line
    cursor = database.cursor()

    # Create the INSERT INTO sql query
    query = """INSERT INTO mdl_exos_recommendation (num_exo, theme) VALUES (%s, %s)"""
#    WHERE NOT EXISTS (SELECT * FROM mdl_exos_recommendation WHERE num_exo=%s AND theme=%s)"""
    
    # Tableau pour stocker les différents savoirs faire associés aux exercices
    tab_sf=[]
    tab_sf.append([])
    num_exo=[]
    theme=[]
    # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
    for r in range(1, sheet1.nrows):
        num_exo = int(sheet1.cell(r,0).value)
        theme = int(sheet1.cell(r,1).value)
        cursor.execute(query,(num_exo,theme))
    for r in range(1, sheet2.nrows):
        tab_sf.append([])
        tab_sf[int(sheet2.cell(r,0).value)].append(int(sheet2.cell(r,1).value))
    
    #Remplissage des savoir_faire
    for r in range(1,sheet1.nrows):
        for j in range(0,len(tab_sf[r])):
            value=tab_sf[r][j]
            cursor.execute("INSERT INTO mdl_exos_recommendation (num_exo, savoir_faire) VALUES (%s,%s)", \
                       (r,value))      
        
    # On supprime le fichier telechargé pour ne pas avoir de conflits lors d'une mise a jour
    #os.remove(".exos/bdd.xlsx")
    
    # Close the cursor
    cursor.close()

    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()
    return render_template()

@app.route('/exos/<filename>')
@lti(request='session', error=error, role='staff', app=app)
def uploaded_exo(filename,lti=lti):
    return render_template('upload_reussit.html',lti=lti)

@app.route('/add', methods=['GET'])
@lti(request='session', error=error, app=app)
def add_form(lti=lti):
    """ Page d'acces pour le lti consumer

    :param lti: the `lti` object from `pylti`
    :return: index page for lti provider
    """
    form = AddForm()
    form.p1.data = randint(1, 9)
    form.p2.data = randint(1, 9)
    return render_template('add.html', form=form)

	
	
@app.route('/teacher',methods=['GET','POST'])
@lti(request='session', error=error, app=app)
def teachers_class(lti=lti):
	[coursename,results] = get_params(lti)
			
	return render_template('displayStuds2.html', results=results, coursename=coursename)
	

def set_debugging():
    """ Debuggage du logging

    """
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

set_debugging()

if __name__ == '__main__':
    """
    For if you want to run the flask development server
    directly
    """
    port = int(os.environ.get("FLASK_LTI_PORT", 5000))
    host = os.environ.get("FLASK_LTI_HOST", "localhost")
    app.run(debug=True, host=host, port=port)
