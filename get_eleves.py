#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import MySQLdb

def get_eleves(lti):
    courseid = lti.user_id
    myDB = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = myDB.cursor()
    results={} #dictionnaire qui sera utilisé pour générer du JSON
    results["eleves"]=[] # Clef eleves qui renvoie toutes les informations sur les élèves
    #Requete sql qui renvoie l'id, le nom de utilisateur ainsi que l'id du cours duquel il provient
    cHandler.execute("SELECT DISTINCT u.id AS userid, u.lastname AS lastname, u.firstname AS firstname\
	FROM mdl_user u\
	JOIN mdl_user_enrolments ue ON ue.userid = u.id\
	JOIN mdl_enrol e ON e.id = ue.enrolid\
	JOIN mdl_role_assignments ra ON ra.userid = u.id\
	JOIN mdl_context ct ON ct.id = ra.contextid AND ct.contextlevel = 50\
	JOIN mdl_course c ON c.id = ct.instanceid AND e.courseid = c.id\
	JOIN mdl_role r ON r.id = ra.roleid AND r.shortname = 'student'\
	WHERE e.status = 0 AND u.suspended = 0 AND u.deleted = 0\
	AND (ue.timeend = 0 OR ue.timeend > NOW()) AND ue.status = 0 AND courseid = %s ORDER BY lastname", courseid)
    res = cHandler.fetchall()    
			
    return res