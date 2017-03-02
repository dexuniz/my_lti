from pylti.flask import lti

def get_params(lti):
	courseid = lti.user_id
	myDB = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="",db="moodle")
	cHandler = myDB.cursor()
	
	#Requete sql qui renvoie l'id, le nom de utilisateur ainsi que l'id du cours duquel il provient
	cHandler.execute("SELECT DISTINCT u.id AS userid, u.lastname AS lastname, c.id AS courseid\
	 FROM mdl_user u\
	 JOIN mdl_user_enrolments ue ON ue.userid = u.id\
	 JOIN mdl_enrol e ON e.id = ue.enrolid\
	 JOIN mdl_role_assignments ra ON ra.userid = u.id\
	 JOIN mdl_context ct ON ct.id = ra.contextid AND ct.contextlevel = 50\
	 JOIN mdl_course c ON c.id = ct.instanceid AND e.courseid = c.id\
	 JOIN mdl_role r ON r.id = ra.roleid AND r.shortname = 'student'\
	 WHERE e.status = 0 AND u.suspended = 0 AND u.deleted = 0\
	 AND (ue.timeend = 0 OR ue.timeend > NOW()) AND ue.status = 0 AND courseid = %s ORDER BY lastname", courseid)
	results = cHandler.fetchall()
	#Conversion en liste necessaire pour modifier results qui est à la base un tulpe
	results = list(results)
	#Requete SQL pour récuperer le nom du cours dans lequel le plugin est implanté
	cHandler.execute("SELECT c.fullname FROM mdl_course c WHERE c.id = %s", courseid)
	coursename=cHandler.fetchall()
	for i in range(0,len(results)):
		id=results[i][0]
		#On convertit les tulpes en listes pour pouvoir ajouter des éléments
		results[i]=list(results[i])
		#On récupère la liste des quiz effectués par l'élève
		cHandler.execute("SELECT quiz FROM mdl_quiz_attempts WHERE userid=%s ORDER BY quiz", id)
		quiz_id=cHandler.fetchall()
		for num in quiz_id:
			p=[(id,),(num,)]
			#Récupération des notes au quiz de numero num
			cHandler.execute("SELECT sumgrades FROM mdl_quiz_attempts WHERE userid=%s AND quiz=%s ORDER BY quiz",(id,num))
			#Rajout d'une colone dans results pour les notes
			results[i].append('Pas de note')
			grades=cHandler.fetchall()
			if len(grades) > 0:
				results[i][3]=grades[0][0]
			## A faire
			
	return [coursename,results]