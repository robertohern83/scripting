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


def updateApplicationFile(appName, contentsPath, contentUri):
    AdminApp.update(appName, 'file', '[-operation update ' + ' -contents ' + contentsPath + ' -contenturi ' + contentUri + ']')



######################Recuperacion de parametros######################

#Argumentos -> Nombre aplicacion, folder de archivo, URI destino
#updateApplicationFile('RedirEAR', 'redir-loadbalancing-config.xml', 'RedirWeb.war/WEB-INF/resources/redir/config/loadBalancing/redir-loadbalancing-config.xml')
#RedirEAR redir-loadbalancing-config.xml RedirWeb.war/WEB-INF/resources/redir/config/loadBalancing/redir-loadbalancing-config.xml

updateApplicationFile(sys.argv[0], sys.argv[1], sys.argv[2])


###############################Salvado################################
print "     Salvando configuraciones."
AdminConfig.save()
print "     Ejecucion de script finalizada."
###############################Salvado################################
