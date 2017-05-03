#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import MySQLdb

def get_params(lti):
    courseid = lti.user_id
    myDB = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
    cHandler = myDB.cursor()
    results={} #dictionnaire qui sera utilisé pour générer du JSON
    results["eleves"]=[] # Clef eleves qui renvoie toutes les informations sur les élèves
    #Requete sql qui renvoie l'id, le nom de utilisateur ainsi que l'id du cours duquel il provient
    cHandler.execute("SELECT DISTINCT u.id AS userid, u.lastname AS lastname, c.id AS courseid, u.firstname AS firstname\
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
    #Requete SQL pour récuperer le nom du cours dans lequel le plugin est implanté
    cHandler.execute("SELECT c.fullname FROM mdl_course c WHERE c.id = %s", courseid)
    coursename=cHandler.fetchall()
    for i in range(0,len(res)):
        id=res[i][0]
    		
        #initialisation
        # results["eleves"].append({})
    		
        #Ajout du nom de l'eleve
        # results["eleves"][i]["nom"]=res[i][1]
        # results["eleves"][i]["id"]=id
        d = { 'nom': res[i][1], 'id': id, 'prenom':res[i][3] }
        results['eleves'].append(d)
        #Liste des identifiants des quiz effectués par l'élève
        cHandler.execute("SELECT quiz FROM mdl_quiz_attempts WHERE userid=%s ORDER BY quiz", id)
    		
        quiz_id=cHandler.fetchall()
    		
        #initialisation
        results["eleves"][i]["quiz"]=[]
    		
        for num in quiz_id:
            num = num[0]
            #Récupération des notes au quiz de numero num
            cHandler.execute("SELECT sumgrades FROM mdl_quiz_attempts WHERE userid=%(userid)s \
                             AND quiz=%(num)s ORDER BY quiz",{'userid':id,'num':num})
    			
    			
            #Récuperation du contenu de la requete
            grades=cHandler.fetchall()
    			
            if len(grades) > 0:
                results["eleves"][i]["quiz"].append((num,float(grades[0][0])))
    			
            ## Retourner du  JSON
    results=json.dumps(results, indent=4)
    with open('data.json', 'w') as f:
        f.write(results)
        f.close()
    with open('data.json','r') as data_file:
        jsondata=json.load(data_file)
    
			
    return [coursename,jsondata]