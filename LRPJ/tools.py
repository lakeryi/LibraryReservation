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