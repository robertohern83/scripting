#Crea los servidores
#gdelgadoh
#version 1.0

import sys
import string
import re


########################################################
# Indica si el server existe
########################################################
def serverExist(serverList, serverName):
    result = None
    if(re.match(serverName, serverList)):
        print serverName      
        result = 1
    else: 
        result = 0
    return result


########################################################
# Retorna un puerto epecífico de un server
########################################################
def getEndPointValue(pNodeName, pServerName, pEndPointName):
	lineSeparator = java.lang.System.getProperty("line.separator")
	nodes=AdminConfig.list("Node").split(lineSeparator) 
	for node in nodes:
	  nodeName = AdminConfig.showAttribute(node, "name")
	  serverEntries  = AdminConfig.list("ServerEntry", node).split(lineSeparator)
	  if (nodeName == pNodeName):
		  for serverEntry in serverEntries:
		    serverName = AdminConfig.showAttribute(serverEntry, "serverName")
		    if (serverName == pServerName):
			    namedEndPoints = AdminConfig.list("NamedEndPoint", serverEntry).split(lineSeparator)
			    for namedEndPoint in namedEndPoints:
			    	endPointName  = AdminConfig.showAttribute(namedEndPoint, "endPointName")
			    	endPoint = AdminConfig.showAttribute(namedEndPoint, "endPoint")
			    	host = AdminConfig.showAttribute(endPoint, "host")
			    	port  = AdminConfig.showAttribute(endPoint, "port")
			        if (endPointName == pEndPointName):
			    	    print "EndPointFound: " + endPointName+ ": " + host + ":" + port
			    	    return port
        return ''    


########################################################
# Creación del cluster
########################################################
def createCluster( nameOfCluster, createReplicationDomain = 0 ):
 	cluster = None
  	# create the cluster
  	print "  . . . creating a " + nameOfCluster + " cluster"
  	if createReplicationDomain == 0:
    		cluster = AdminTask.createCluster('[-clusterConfig [-clusterName ' + nameOfCluster + ']]')
  	else:
    		cluster = AdminTask.createCluster('[-clusterConfig [-clusterName ' + nameOfCluster + '] -replicationDomain [-createDomain true] ]')
  	print cluster
  	#whatFilesChanged()
  	return

########################################################
# Creación de miembros del cluster
########################################################
def createFirstClusterMember( nameOfCluster, nodeName, serverName, joinReplicationDomain = 0, nodeGroupName = "DefaultNodeGroup", coreGroupName = "DefaultCoreGroup" ):
	replicate = 'false'

    	print "Adding first member " + nodeName + " / " + serverName + " to " + nameOfCluster
    	if joinReplicationDomain != 0:
    		 replicate = 'true'
    	print AdminTask.createClusterMember('[-clusterName ' + nameOfCluster +
        ' -memberConfig [-memberNode ' + nodeName + ' -memberName ' + serverName +
        ' -replicatorEntry ' + replicate   + '] ' +
        ' -firstMember[ -templateName default -nodeGroup ' + nodeGroupName +
        '  -coreGroup ' + coreGroupName + '   ] ' + ']')

def whatFilesChanged():
  	print "The following congfiguration files have changes pending:"
  	print AdminConfig.queryChanges()
  	return

def createAdditionalClusterMembers( nameOfCluster, listOfServerNames ):	
	listOfProposedNewMemberServers = list( listOfServerNames )
	print "  . . . adding " + str( len(listOfProposedNewMemberServers) ) + " additional members to the " + nameOfCluster + " cluster"
	
	# add the rest of the cluster members
	for server in listOfProposedNewMemberServers:
		nodeName = server[0]
		serverName = server[1]
		replicate = "false"
		if len( server ) == 2:
			print AdminTask.createClusterMember('[-clusterName ' + nameOfCluster + ' -memberConfig [-memberNode ' + nodeName + ' -memberName ' + serverName  + ']]')
		if len( server ) == 3:
			# convert the ReplicationDomain parameter of our parameter list
			# into the 'true' or 'false' notation that AdminTask requires
			if server[2] == 0:
				replicate = "false"
			else:
				replicate = "true"
			print AdminTask.createClusterMember('[-clusterName ' + nameOfCluster + ' -memberConfig [-memberNode ' + nodeName + ' -memberName ' + serverName + ' -replicatorEntry ' + replicate + ']]')
	return

########################################################
# Funcion para crear un servidor
########################################################
def createServer(nodeName, name):
    #nodeContext = AdminConfig.getid(node)
    print 'Creating server ' + name + ' on ' + nodeName
    print AdminTask.createApplicationServer(nodeName, ['-name', name, '-templateName', 'default'])
    #print AdminConfig.create('Server', nodeContext, ['name', name])


########################################################
# Funcion que crea los cluster
########################################################
def createClusters(cName, node, baseName, serverList):
	print 'Start cluster creation'
	try:
		createCluster( cName, 0 )
		print 'Cluster ' + cName +' created'
	except:
		print "Error creating cluster ", sys.exc_info()[0], sys.exc_info()[1]

	print 'Start members creation'
	try:
		createFirstClusterMember( cName, node, baseName + '1', 0, "DefaultNodeGroup", "DefaultCoreGroup" )
	except:
		print "Error creating first cluster member ", sys.exc_info()[0], sys.exc_info()[1]
	
	try:
		createAdditionalClusterMembers(cName, serverList)
	except:
		print "Error creating additional custer members ", sys.exc_info()[0], sys.exc_info()[1]

	


########################################################
# Funcion que crea el virtual host
########################################################
def createVirtualHost(nodoName, virtualHost, hostAlias, serversQuantity, serverBaseName):
	print 'Start virtual host creation'
	servers = AdminConfig.list('Server').splitlines()

	#print 'Parametros de createVirtualHost'
	#print 'nodoName: ' + nodeName
	#print 'virtualHost: ' + virtualHost
	#print 'hostAlias: ' + hostAlias
	#print 'serversQuantity: ' + str(serversQuantity)
	#print 'serverBaseName: ' + serverBaseName

	print 'Creando el virtual host ' + virtualHost
	try:
		AdminConfig.create('VirtualHost', AdminConfig.getid('/Cell:' + AdminControl.getCell() + '/'), '[[name ' + virtualHost + ']]') 
		print 'Virtual host creado'
	except:
		print "Error creando el virtual host ", sys.exc_info()[0], sys.exc_info()[1]

	for x in range(0, serversQuantity):
		server = serverBaseName + str(x+1)
		#print 'server: ' + server
		portHttp = getEndPointValue(nodeName, server, 'WC_defaulthost')		
		#print 'portHttp: ' + portHttp
		AdminConfig.create('HostAlias', AdminConfig.getid('/Cell: ' + AdminControl.getCell() + '/VirtualHost:'+ virtualHost +'/'), '[[port ' + portHttp + '] [hostname ' + hostAlias + ']]')
		print 'Host Alias ' + hAlias + ' agregado en el puerto ' + portHttp
		portHttps = getEndPointValue(nodeName, server, 'WC_defaulthost_secure')
		#print 'portHttps: ' + portHttps
		AdminConfig.create('HostAlias', AdminConfig.getid('/Cell: ' + AdminControl.getCell() + '/VirtualHost:'+ virtualHost +'/'), '[[port ' + portHttps + '] [hostname ' + hostAlias + ']]')
		print 'Host Alias ' + hAlias + ' agregado en el puerto ' + portHttps


		
## Creación de los servers

#Argumentos -> Nodo, NombreBase, Cantidad de Servers, Nombre de Cluster, Virtual Host, Host Alias
if ( len(sys.argv) == 6 ):
	nodeName = sys.argv[0]
	pppBaseName = sys.argv[1]
	pppServerQuantity = int(sys.argv[2])
	clusterName = sys.argv[3]
	vhost = sys.argv[4]
	hAlias = sys.argv[5]
	pppServerListMembers = []

	for x in range (1, pppServerQuantity):
		try:	
			pppServerName = pppBaseName + str(x+1)
			pppServerListMembers.append((nodeName, pppServerName))		
			#createServer(nodeName, pppServerName)		
		except:
			print "Error en la creación del servidor ", sys.exc_info()[0], sys.exc_info()[1]


	# Creacion del cluster
	try:
		createClusters(clusterName, nodeName, pppBaseName, pppServerListMembers)
	except:
		print "Error en la creación del cluster ", sys.exc_info()[0], sys.exc_info()[1]

	# Crea el virtual host
	try:
			createVirtualHost(nodeName, vhost, hAlias, pppServerQuantity, pppBaseName)
	except:
		print "Error en la creación del virtual host ", sys.exc_info()[0], sys.exc_info()[1]

	###############################Salvado################################
	print "Salvando configuraciones."
	AdminConfig.save()
	print "Ejecución de script finalizada."
	###############################Salvado################################
else: 
	print 'Cantidad de parámetros incorrecta, favor validar.'