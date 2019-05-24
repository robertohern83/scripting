#rhernandezm
#versión 1.0
#creación de recursos del servidor de BAC Payments Offline

import sys
import string


#Funcion base para obtener parametros. 
def getInputParameter(message, default, ignorecase):
	print '**************************************************************'
	if(default != '**undefined**'):
		print message + ' (El valor default es: ' + default + '):'
	else:
		print message + ' (*Requerido*):'

	parameter = sys.stdin.readline()
	if(parameter == '\n' or parameter == ''):
		if(default != '**undefined**'):
			parameter = default
		else:
			while (parameter == '\n' or parameter == ''):
				print 'El parametro no puede ser nulo pues no tiene default'
				parameter = sys.stdin.readline()
			
	if(ignorecase):
		parameter = string.upper(parameter)
	parameter = string.replace(parameter, '\n', '')
	print 'Valor seleccionado: ' + parameter
	print '**************************************************************'
	return parameter


def updateApplicationWeight(appname, weight):
    dep = AdminConfig.getid("/Deployment:"+ appname +"/")
    print dep
    print ''
    depObject = AdminConfig.showAttribute(dep, "deployedObject")
    print depObject
    print ''
    print "[['startingWeight', '"+ weight +"']]"
    AdminConfig.modify(depObject, [['startingWeight', weight]])



######################Recuperacion de parametros######################

#Argumentos -> Nodo, Server, Ruta Archivo, Nombre aplicacion, virtualhost
updateApplicationWeight(sys.argv[0], sys.argv[1])

###############################Salvado################################
print "     Salvando configuraciones."
AdminConfig.save()
print "     Ejecucion de script finalizada."
###############################Salvado################################
