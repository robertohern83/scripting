import sys
import time

clustername = sys.argv[0]
retries = int(sys.argv[1])



def isClusterStarted (clusterNameParam, retriesParameter):
    clusterObject = AdminControl.completeObjectName("type=Cluster,name="+ clustername +",*" )
    running = "websphere.cluster.running"
    isStarted = 0
    retriesCounter = 0
    while (not isStarted) and (retriesCounter < retriesParameter):
        clusterStatus = AdminControl.getAttribute(clusterObject, "state" )
        print clusterStatus
        retriesCounter = retriesCounter + 1
        if (cmp(clusterStatus, running) == 0):
            isStarted = 1
            print 'Iniciado'
        else:
            print 'No iniciado, reintentando consulta...'
        time.sleep(60)


    return isStarted


result = isClusterStarted(clustername, retries)

if(not result):
    raise Exception('EL CLUSTER NO INICIO A TIEMPO')        

sys.exit()
