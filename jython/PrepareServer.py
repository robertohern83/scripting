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


def syncAndRestartServer(nodeName, serverName, cluster):
    Sync1 = AdminControl.completeObjectName('type=NodeSync,process=nodeagent,node=' + nodeName + ',*')
    syncResult = AdminControl.invoke(Sync1, 'sync')
    
    if(not syncResult):
        raise Exception('Error al sincronizar el nodo')
    
    
    try:
		if(cluster is None):
			try:
				AdminControl.stopServer(serverName, nodeName)
			except:
				print 'Error al detener el server'
			
			print 'Starting server ' + serverName
			print AdminControl.startServer(serverName, nodeName, 500)
			print 'Server ' + serverName + ' Started'
		else:
			cellName = AdminControl.getCell()
			print 'cell=' + cellName + ',type=Cluster,name=' + cluster + ',*'
			#print 'cell=CRCORVWASNDDESACellSecStg,type=Cluster,name=' + cluster + ',*'
			clusterObject = AdminControl.completeObjectName('cell=' + cellName + ',type=Cluster,name=' + cluster + ',*')
			#clusterObject = AdminControl.completeObjectName('cell=CRCORVWASNDDESACellSecStg,type=Cluster,name=' + cluster + ',*')
			print 'Restarting cluster ' + cluster
			AdminControl.invoke(clusterObject, 'rippleStart')
    except BaseException:
        print 'Error al desinstalar la aplicacion'
    


######################Recuperacion de parametros######################

if(len(sys.argv) == 2):
	syncAndRestartServer(sys.argv[0], sys.argv[1], None)
else:
	syncAndRestartServer(sys.argv[0], sys.argv[1], sys.argv[2])


