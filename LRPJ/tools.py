#from library_reservation import models
import string

def isset(v): 
	try : 
		type(eval(v)) 
	except : 
		return 0 
	else : 
		return 1

def html_printable(s):
	#s = s.replace(' ','_')
	s = s.replace('\n','FudanFudan')
	return s

"""
def query_user(ID):
	s = models.Students.objects.all().filter(student_id = ID)
	name = s.values_list('name', flat = True)[0]
	psw = s.values_list('password', flat = True)[0]
	request.session['user_name'] = name
	age = str(s.values_list('age', flat = True)[0])
	sex = s.values_list('sex', flat = True)[0]
	major = s.values_list('major', flat = True)[0]
	if sex == 'M':
		sex = '男'
	else:
		sex = '女'
	ret = {'ID' : ID, 'psw' : psw, 'name' : name, 'age' : age, 'sex' : sex, 'major' : major}
	return ret
"""