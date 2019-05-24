#Crea los recursos jms
#gdelgadoh
#version 1.0


## Funcion para crear un recurso de Cola
def createMQQueue(context, name, jndiName, queueName, useRFH2):
    print 'createMQQueue: ' + name 
    contextId = AdminConfig.getid(context)
    AdminTask.createWMQQueue(contextId, ["-jndiName", jndiName , "-qmgr", "null" , "-queueName", queueName , "-name", name, "-useRFH2",  useRFH2])


## Funcion para crear un recurso de QCF
def createBindingsMQQueueConnectionFactory(context, name, jndiName, queueMgrName, connectionPoolProperties, sessionPoolProperties):
    print 'createBindingsMQQueueConnectionFactory: ' + name

    id = '/Node:' + context + '/'

    contextId = AdminConfig.getid(context)
    createdResource = AdminTask.createWMQConnectionFactory(contextId, ["-name "+ name + " -jndiName "+ jndiName + " -type QCF " + " -qmgrName " + queueMgrName + " -wmqTransportType BINDINGS"])
    AdminConfig.modify(createdResource, [["connectionPool", connectionPoolProperties], ["sessionPool", sessionPoolProperties]])



#Argumentos -> Nodo, QueueManager
		
## Creación de las colas y QCFs

nodeContext = '/Node:' + sys.argv[0] + '/'
#nodeContext = sys.argv[0]
queueManager = sys.argv[1]

print 'Starting Creating MQ Queues'

print 'nodeContext: ' + nodeContext

try:
	## Cola de respuesta
	createMQQueue(nodeContext, "BCO.SRV.RESPUESTA", "jms/BCO.SRV.RESPUESTA", "CL.CRI400W.RESPUESTA.KSEC", "false")
except:
	print "Error en la creación de la cola ", sys.exc_info()[0], sys.exc_info()[1]

try:
	## Cola de Costa Rica
	createMQQueue(nodeContext, "CL.LCRBA.SRV.CONSULTA.FRM3", "jms/CL.LCRBA.SRV.CONSULTA.FRM3", "CL.LCRBA.SRV.CONSULTA.FRM3.VT", "false")
except:
	print "Error en la creación de la cola ", sys.exc_info()[0], sys.exc_info()[1]	

try:
	## Cola de Honduras
	createMQQueue(nodeContext, "CL.LHNBA.SRV.CONSULTA.FRM3", "jms/CL.LHNBA.SRV.CONSULTA.FRM3", "CL.LCRBA.SRV.CONSULTA.FRM3.VT", "false")
except:
	print "Error en la creación de la cola ", sys.exc_info()[0], sys.exc_info()[1]

try:
	## Cola de El Salvador
	createMQQueue(nodeContext, "CL.LSVBA.SRV.CONSULTA.FRM3", "jms/CL.LSVBA.SRV.CONSULTA.FRM3", "CL.LCRBA.SRV.CONSULTA.FRM3.VT", "false")
except:
	print "Error en la creación de la cola ", sys.exc_info()[0], sys.exc_info()[1]

try:
	## Cola de Nicaragua
	createMQQueue(nodeContext, "CL.LNIBA.SRV.CONSULTA.FRM3", "jms/CL.LNIBA.SRV.CONSULTA.FRM3", "CL.LCRBA.SRV.CONSULTA.FRM3.VT", "false")
except:
	print "Error en la creación de la cola ", sys.exc_info()[0], sys.exc_info()[1]

try:
	## Cola de Guatemala
	createMQQueue(nodeContext, "CL.LGTBA.SRV.CONSULTA.FRM3", "jms/CL.LGTBA.SRV.CONSULTA.FRM3", "CL.LCRBA.SRV.CONSULTA.FRM3.VT", "false")
except:
	print "Error en la creación de la cola ", sys.exc_info()[0], sys.exc_info()[1]

try:
	## Cola de Panama
	createMQQueue(nodeContext, "CL.LPABA.SRV.CONSULTA.FRM3", "jms/CL.LPABA.SRV.CONSULTA.FRM3", "CL.LCRBA.SRV.CONSULTA.FRM3.VT", "false")
except:
	print "Error en la creación de la cola ", sys.exc_info()[0], sys.exc_info()[1]

try:
	## Cola de Bahamas
	createMQQueue(nodeContext, "CL.LBHBA.SRV.CONSULTA.FRM3", "jms/CL.LBHBA.SRV.CONSULTA.FRM3", "CL.LCRBA.SRV.CONSULTA.FRM3.VT", "false")
except:
	print "Error en la creación de la cola ", sys.exc_info()[0], sys.exc_info()[1]
print 'MQ Queues Created\n\n'


#### Creacion de los QCFs
print 'Starting Creating Connection Factories'

try:
	## QCF para Costa Rica
	createBindingsMQQueueConnectionFactory(nodeContext, "BCOSRVQCF", "jms/BCOSRVQCF", queueManager, [['maxConnections', '20'], ['minConnections', '5'], ['connectionTimeout', '180']], [['maxConnections', '30'], ['minConnections', '5'], ['connectionTimeout', '180']])
except:
	print "Error en la creación del QCF ", sys.exc_info()[0], sys.exc_info()[1]

try:
	## QCF para El Salvador
	createBindingsMQQueueConnectionFactory(nodeContext, "BCOSVSRVQCF", "jms/BCOSVSRVQCF", queueManager, [['maxConnections', '20'], ['minConnections', '5'], ['connectionTimeout', '180']], [['maxConnections', '30'], ['minConnections', '5'], ['connectionTimeout', '180']])
except:
	print "Error en la creación del QCF ", sys.exc_info()[0], sys.exc_info()[1]

try:
	## QCF para Honduras
	createBindingsMQQueueConnectionFactory(nodeContext, "BCOHNSRVQCF", "jms/BCOHNSRVQCF", queueManager, [['maxConnections', '20'], ['minConnections', '5'], ['connectionTimeout', '180']], [['maxConnections', '30'], ['minConnections', '5'], ['connectionTimeout', '180']])
except:
	print "Error en la creación del QCF ", sys.exc_info()[0], sys.exc_info()[1]	

try:
	## QCF para Nicaragua
	createBindingsMQQueueConnectionFactory(nodeContext, "BCONISRVQCF", "jms/BCONISRVQCF", queueManager, [['maxConnections', '20'], ['minConnections', '5'], ['connectionTimeout', '180']], [['maxConnections', '30'], ['minConnections', '5'], ['connectionTimeout', '180']])
except:
	print "Error en la creación del QCF ", sys.exc_info()[0], sys.exc_info()[1]		

try:
	## QCF para Guatemala
	createBindingsMQQueueConnectionFactory(nodeContext, "BCOGTSRVQCF", "jms/BCOGTSRVQCF", queueManager, [['maxConnections', '20'], ['minConnections', '5'], ['connectionTimeout', '180']], [['maxConnections', '30'], ['minConnections', '5'], ['connectionTimeout', '180']])
except:
	print "Error en la creación del QCF ", sys.exc_info()[0], sys.exc_info()[1]			

try:
	## QCF para Panama
	createBindingsMQQueueConnectionFactory(nodeContext, "BCOPASRVQCF", "jms/BCOPASRVQCF", queueManager, [['maxConnections', '20'], ['minConnections', '5'], ['connectionTimeout', '180']], [['maxConnections', '30'], ['minConnections', '5'], ['connectionTimeout', '180']])
except:
	print "Error en la creación del QCF ", sys.exc_info()[0], sys.exc_info()[1]				

try:
	## QCF para Kayman
	createBindingsMQQueueConnectionFactory(nodeContext, "BCOKYSRVQCF", "jms/BCOKYSRVQCF", queueManager, [['maxConnections', '20'], ['minConnections', '5'], ['connectionTimeout', '180']], [['maxConnections', '30'], ['minConnections', '5'], ['connectionTimeout', '180']])
except:
	print "Error en la creación del QCF ", sys.exc_info()[0], sys.exc_info()[1]		

try:
	## QCF para Bahamas
	createBindingsMQQueueConnectionFactory(nodeContext, "BCOBHSRVQCF", "jms/BCOBHSRVQCF", queueManager, [['maxConnections', '20'], ['minConnections', '5'], ['connectionTimeout', '180']], [['maxConnections', '30'], ['minConnections', '5'], ['connectionTimeout', '180']])
except:
	print "Error en la creación del QCF ", sys.exc_info()[0], sys.exc_info()[1]			


print 'Connection Factories Created\n\n'


###############################Salvado################################
print "Salvando configuraciones."
AdminConfig.save()
print "Ejecución de script finalizada."
###############################Salvado################################