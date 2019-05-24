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


def installApplication(nodeName, serverName, path, appname, virtualHost, cluster):

    try:
        AdminApp.uninstall(appname)
    except:
        print 'Error al desinstalar la aplicacion'
    
    if(cluster is None):
		AdminApp.install(path, ['-server', serverName, '-node', nodeName, '-appname', appname, '-MapWebModToVH', [['.*', '.*', virtualHost]]])
		print path + ' deployed on server ' + serverName
    else:
		AdminApp.install(path, ['-cluster', cluster, '-node', nodeName, '-appname', appname, '-MapWebModToVH', [['.*', '.*', virtualHost]]])
		print path + ' deployed on cluster ' + cluster

def updateApplicationFile(appName, contentsPath, contentUri):
    AdminApp.update(appName, 'file', '[-operation update ' + ' -contents ' + contentsPath + ' -contenturi ' + contentUri + ']')



######################Recuperacion de parametros######################

#Argumentos -> Nodo, Server, Ruta Archivo, Nombre aplicacion, virtualhost
#installApplication('SEC3Node', 'SEC3Server', 'RedirEar.ear', 'RedirEAR', 'redir_host')
#SEC3Node SEC3Server RedirEar.ear RedirEAR redir_host

if (len(sys.argv) == 5):
	installApplication(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], None)
else:
	installApplication(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

###############################Salvado################################
print "     Salvando configuraciones."
AdminConfig.save()
print "     Ejecucion de script finalizada."
###############################Salvado################################
