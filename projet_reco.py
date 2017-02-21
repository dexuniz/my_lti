#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import sys
import requests
from flask import Flask, redirect,url_for , send_from_directory, render_template
from flask import render_template
import urllib
import sqlite3
from pylti.flask import lti
import MySQLdb

VERSION = '0.0.5'
app = Flask(__name__)
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


@app.route('/grade', methods=['POST'])
@lti(request='session', error=error, app=app)
def grade(lti=lti):
    """ Test pour poster une note

    :param lti: the `lti` object from `pylti`
    :return: grade rendered by grade.html template
    """
    form = AddForm()
    correct = ((form.p1.data + form.p2.data) == form.result.data)
    form.correct.data = correct
    #lti.post_grade(1 if correct else 0)
    return render_template('grade.html', form=form)
	
	
@app.route('/teacher',methods=['GET','POST'])
@lti(request='session', error=error, app=app)
def teachers_class(lti=lti):
	courseid = lti.user_id
	myDB = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
	cHandler = myDB.cursor()
	
	
	cHandler.execute("SELECT DISTINCT u.id AS userid, u.lastname AS lastname, c.id AS courseid\
	 FROM mdl_user u\
	 JOIN mdl_user_enrolments ue ON ue.userid = u.id\
	 JOIN mdl_enrol e ON e.id = ue.enrolid\
	 JOIN mdl_role_assignments ra ON ra.userid = u.id\
	 JOIN mdl_context ct ON ct.id = ra.contextid AND ct.contextlevel = 50\
	 JOIN mdl_course c ON c.id = ct.instanceid AND e.courseid = c.id\
	 JOIN mdl_role r ON r.id = ra.roleid AND r.shortname = 'student'\
	 WHERE e.status = 0 AND u.suspended = 0 AND u.deleted = 0\
	 AND (ue.timeend = 0 OR ue.timeend > NOW()) AND ue.status = 0 AND courseid = %s", courseid)
	results = cHandler.fetchall()
	results = list(results)
	cHandler.execute("SELECT c.fullname FROM mdl_course c WHERE c.id = %s", courseid)
	coursename=cHandler.fetchall()
	for i in range(0,len(results)-1):
		id=results[i][0]
		results[i]=list(results[i])
		results[i].append('1')
		
		cHandler.execute("SELECT sumgrades FROM mdl_quiz_attempts WHERE userid=%s ORDER BY timemodified DESC", id)
		#A mod
		results[i][3]=cHandler.fetchall()[0][0]
	#Accès à la base de donnée locale du plugin
			## A faire
			
	return render_template('displayStuds.html', results=results, coursename=coursename)
	
""" N'est plus d'actualité, on peut récuperer l'id du cours via lti 
# @app.route('/students_related',methods=['GET','POST'])
# @lti(request='session', error=error, app=app)
# def get_studs(lti=lti):

	# course_number=4
	# myDB = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
	# cHandler = myDB.cursor()
    cHandler.execute("SELECT 
	cHandler.execute("SELECT defaultgroupingid FROM mdl_course WHERE fullname='Recommendation'")
	Liste des étudiants du cours sous la forme (userid, lastname, course id)
	# cHandler.execute("SELECT DISTINCT u.id AS userid, u.lastname AS lastname, c.id AS courseid\
	 # FROM mdl_user u\
	 # JOIN mdl_user_enrolments ue ON ue.userid = u.id\
	 # JOIN mdl_enrol e ON e.id = ue.enrolid\
	 # JOIN mdl_role_assignments ra ON ra.userid = u.id\
	 # JOIN mdl_context ct ON ct.id = ra.contextid AND ct.contextlevel = 50\
	 # JOIN mdl_course c ON c.id = ct.instanceid AND e.courseid = c.id\
	 # JOIN mdl_role r ON r.id = ra.roleid AND r.shortname = 'student'\
	 # WHERE e.status = 0 AND u.suspended = 0 AND u.deleted = 0\
	 # AND (ue.timeend = 0 OR ue.timeend > NOW()) AND ue.status = 0 AND courseid = %s", course_number)
	cHandler.execute("SELECT id FROM mdl_user_enrolments WHERE mdl_user_enrolments.enrolid = '7L'")
	cHandler.execute("SELECT lastname FROM mdl_user WHERE mdl_user.id = 2 OR mdl_user.id = 3")
	cHandler.execute("SELECT * FROM information_schema.tables WHERE TABLE_TYPE='BASE TABLE'")
	# results = cHandler.fetchall()
	# return render_template('photo.html', results=results)	
"""		
""" Filtre html pour récuperer les élèves d'un cours, non utilisé pour le moment """
@app.template_filter('get_students_from_course')
@lti(request='session', error=error, app=app)
def get_studs(course_number):

	course_number=(course_number,)
	myDB = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
	cHandler = myDB.cursor()
	#cHandler.execute("SELECT 
	#cHandler.execute("SELECT defaultgroupingid FROM mdl_course WHERE fullname='Recommendation'")
	#Liste des étudiants du cours sous la forme (userid, lastname, course id)
	cHandler.execute("SELECT DISTINCT u.id AS userid, u.lastname AS lastname, c.id AS courseid\
	 FROM mdl_user u\
	 JOIN mdl_user_enrolments ue ON ue.userid = u.id\
	 JOIN mdl_enrol e ON e.id = ue.enrolid\
	 JOIN mdl_role_assignments ra ON ra.userid = u.id\
	 JOIN mdl_context ct ON ct.id = ra.contextid AND ct.contextlevel = 50\
	 JOIN mdl_course c ON c.id = ct.instanceid AND e.courseid = c.id\
	 JOIN mdl_role r ON r.id = ra.roleid AND r.shortname = 'student'\
	 WHERE e.status = 0 AND u.suspended = 0 AND u.deleted = 0\
	 AND (ue.timeend = 0 OR ue.timeend > NOW()) AND ue.status = 0 AND courseid = ?", course_number)
	#cHandler.execute("SELECT id FROM mdl_user_enrolments WHERE mdl_user_enrolments.enrolid = '7L'")
	#cHandler.execute("SELECT lastname FROM mdl_user WHERE mdl_user.id = 2 OR mdl_user.id = 3")
	#cHandler.execute("SELECT * FROM information_schema.tables WHERE TABLE_TYPE='BASE TABLE'")
	results = cHandler.fetchall()
	
	return render_template('photo.html', results=results)


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
