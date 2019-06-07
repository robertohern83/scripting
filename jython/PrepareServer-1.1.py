import sys
import string
import time


def syncAndRestartServer(nodeName, serverName, cluster):
    Sync1 = AdminControl.completeObjectName('type=NodeSync,process=nodeagent,node=' + nodeName + ',*')
    syncResult = AdminControl.invoke(Sync1, 'sync')
    #time.sleep(60)
    
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
		clusterObject = AdminControl.completeObjectName('cell=' + cellName + ',type=Cluster,name=' + cluster + ',*')
		print 'Starting cluster ' + cluster
		AdminControl.invoke(clusterObject, 'start')
		#rippleStart
    except:
        print 'Error al desinstalar la aplicacion'



def isClusterStopped (clusterNameParam, retriesParameter):
    clusterObject = AdminControl.completeObjectName("type=Cluster,name="+ clusterNameParam +",*" )
    stopped = "websphere.cluster.stopped"
    isStopped = 0
    retriesCounter = 0
    while (not isStopped) and (retriesCounter < retriesParameter):
        clusterStatus = AdminControl.getAttribute(clusterObject, "state" )
        print clusterStatus
        retriesCounter = retriesCounter + 1
        if (cmp(clusterStatus, stopped) == 0):
            isStopped = 1
            print 'Detenido'
        else:
            print 'No se ha detenido, reintentando consulta...'
            time.sleep(60)
    return isStopped


def stopCluster(cluster):  
	cellName = AdminControl.getCell()
	print 'cell=' + cellName + ',type=Cluster,name=' + cluster + ',*'
	clusterObject = AdminControl.completeObjectName('cell=' + cellName + ',type=Cluster,name=' + cluster + ',*')
	print 'Stopping cluster ' + cluster
	AdminControl.invoke(clusterObject, 'stop')
	#rippleStart
	isStopped = isClusterStopped (cluster, 20)
	if not isStopped:
		raise Exception('Error al detener el server - El server no se detuvo en el tiempo adecuado')

def returnBooleanValue(stringValue):
	if (cmp(stringValue, 'false') == 0):
		return 0;
	
	if (cmp(stringValue, 'true') == 0):
		return 1;
	else:
		return 1;

def restartNodeAgent(nodeName, retriesParameter):
	retriesCounter = 0
	print "Obteniendo el nodeAgent"
	na = AdminControl.queryNames('type=NodeAgent,node=' + nodeName + ',*')
	print na
    	print AdminControl.invoke(na,'restart','false false')
    	print "Reiniciado...."
    	time.sleep(60)
      
    
def syncChanges(nodeName, retriesParameter):
    print "tratando de sincronizar ...." + nodeName
    Sync1 = AdminControl.completeObjectName('type=NodeSync,process=nodeagent,node=' + nodeName + ',*')
    syncStatus = 0
    retriesCounter = 0
    
    while (not syncStatus) and (retriesCounter < retriesParameter):
    	retriesCounter = retriesCounter + 1
    	syncResult = AdminControl.invoke(Sync1, 'sync')
    	print "Resultado de la sincronizacion: " + syncResult
    	print "Esperando 30 segundos para completar la sincronizacion antes de liberar el hilo.."
    	time.sleep(30)
    	syncStringStatus = AdminControl.invoke(Sync1, 'isNodeSynchronized')
    	print "Estado de la sincronizacion: " + syncStringStatus
    	syncStatus = returnBooleanValue(syncResult) and returnBooleanValue(syncStringStatus)
    	
    
    if(not syncStatus):
    	restartNodeAgent(nodeName, retriesParameter)
    
    retriesCounter = 0
    
    while (not syncStatus) and (retriesCounter < retriesParameter):
	retriesCounter = retriesCounter + 1
	syncResult = AdminControl.invoke(Sync1, 'sync')
	print "Resultado de la sincronizacion: " + syncResult
	print "Esperando 30 segundos para completar la sincronizacion antes de liberar el hilo.."
	time.sleep(30)
	syncStringStatus = AdminControl.invoke(Sync1, 'isNodeSynchronized')
	print "Estado de la sincronizacion: " + syncStringStatus
    	syncStatus = returnBooleanValue(syncResult) and returnBooleanValue(syncStringStatus)
    	
    if(not syncStatus):
    	raise Exception('No se logro sincronizar el nodo')
	



######################Recuperacion de parametros######################
if(len(sys.argv) >= 1):
	if( cmp(sys.argv[0], 'stop') == 0):
		print "Detener"
		stopCluster(sys.argv[1])
	if( cmp(sys.argv[0], 'start') == 0):
		print "Iniciar"
		syncAndRestartServer(sys.argv[1], sys.argv[2], sys.argv[3])
	if( cmp(sys.argv[0], 'syncAndRestartServer') == 0):
		print "syncAndRestartServer"
		syncAndRestartServer(sys.argv[1], sys.argv[2], None)
	if( cmp(sys.argv[0], 'sync') == 0):
		print "Sincronizar"
		syncChanges(sys.argv[1], 6)
else: 
	raise Exception('No hay una opcion seleccionada')
		


