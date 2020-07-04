import os
import sys
import pickle
from prettytable import PrettyTable

def flattenList(data):
        results = []
        for rec in data:
            if isinstance(rec, list):
                results.extend(rec)
                results = flattenList(results)
            else:
                results.append(rec)
        return list(results)

class NDUtility:

    def __init__(self, dir_p):
        #self.dir_p = os.path.dirname(os.path.realpath(__file__))+dir_p
        #print (dir_p)
        with open(dir_p+"/NodeDirectory.txt", "rb") as fp:
            self.node = pickle.load(fp)

    def get_allNodes(self):
        #global node
        allNodes = []
        for cluster in self.node.keys():
            allNodes.append(list(self.node[cluster]))
            #print (list(allNodes))
        return list(flattenList(allNodes))

    def get_dict(self):
        return self.node

    def get_allClusters(self):
        #global node
        allClusters = []
        for cluster in self.node.keys():
            allClusters.append(cluster)
        return list(allClusters)

    def get_cluster(self, nodeName):
        for cluster in self.node:
            if nodeName in self.node[cluster]:
                return str(cluster)

    def get_clusterNodes(self, clusterno):
        nodelist = []
        for cluster in self.node:
            if cluster == clusterno:
                return list(list(self.node[cluster]))

    def get_ip(self, nodeName):
        for cluster in self.node:
            if nodeName in self.node[cluster]:
                return str(self.node[cluster][nodeName]['ip'])

    def get_id(self, nodeName):
        for cluster in list(self.node):
            if nodeName in list(self.node[cluster]):
                return str(self.node[cluster][nodeName]['node'])

    def get_rate(self, nodeName):
        for cluster in self.node:
            if nodeName in self.node[cluster]:
                return str(self.node[cluster][nodeName]['rate'])

def get_bwLine(fileName, nodeName):
        bw = ''
        if os.path.isfile(fileName):
            with open(fileName, 'r+') as f:
                lines = f.readlines()
                for i in range(0, len(lines)):
                    line = lines[i]
                    #print(fileName)
                    if (nodeName+"-eth0:") in line:
                        #print(line)
                        Val = (lines[i+1]).split()[8]
                        dataB = (lines[i+1]).split()[9]
                        #Valk = 0
                        if dataB == 'MiB':
                            #print (lines[i+1])
                            #print(nodeName+" has in "+Val+" Mib")
                            Val = float(Val) * 1024
                        #else:
                        #    Valk = Val
                        #print(fileName+' '+nodeName+'Val '+str(Val)+' dataB '+ str(dataB))
                        #print(fileName+' '+nodeName+)
                        return Val, dataB #Send val in KB
                        break
        else:
            return 0.0, 'MiB'

def newget_BwKbTotal(folder, testfor, ND4bw):
    BwTotal = []
    BwControl = []
    BwData = []
    t = PrettyTable()
    t.title = str(testfor)
    t.field_names = ['Node', 'Total', 'Control', 'Data']
    for node in ND4bw.get_allNodes():
        ControlValue, ControloriginalVal = get_bwLine(folder+'/'+testfor+'/'+'BWLogs/'+node+'_bwLogsControl', node)
        TotalValue, TotaloriginalVal = get_bwLine(folder+'/'+testfor+'/'+'BWLogs/'+node+'_bwLogsData', node)
        DataValue = float(TotalValue) - float(ControlValue)
        BwTotal.append(float(TotalValue))
        BwControl.append(float(ControlValue))
        BwData.append(float(DataValue))
        if ND4bw.get_id(node)=='a':
            t.add_row([node+'(Edge)', str(TotalValue)+'('+ND4bw.get_rate(node)+')', ControlValue, DataValue])
        else:
            t.add_row([node, str(TotalValue)+'('+ND4bw.get_rate(node)+')', ControlValue, DataValue])
    TotalBW = float(sum(BwTotal, (0.0)) / 1024)
    TotalBWControl = float(sum(BwControl, (0.0)) / 1024)
    TotalBWData = float(sum(BwData, (0.0)) / 1024)
    t.sortby = "Data"
    t.add_row(['Total MB', str(TotalBW), str(TotalBWControl), str(TotalBWData)])
    print(t)
    return TotalBW, TotalBWControl, TotalBWData

ExpFolder = sys.argv[1]
dataDiff = []
for ExpJobs in (os.listdir(ExpFolder)):
    print('*****************************************************************')
    print('')
    print ExpJobs
    #DTBW, DCBW, DDBW = newget_BwKbTotal(ExpFolder+'/'+ExpJobs, 'dev', NDUtility(ExpFolder+'/'+ExpJobs))
    #BTBW, BCBW, BDBW = newget_BwKbTotal(ExpFolder+'/'+ExpJobs, 'base', NDUtility(ExpFolder+'/'+ExpJobs))
    print('')
    print('\t\t--->BASE<---')
    print('')
    BTBW, BCBW, BDBW = newget_BwKbTotal(ExpFolder+'/'+ExpJobs, 'base', NDUtility(ExpFolder+'/'+ExpJobs))
    #print("Base Total:"+str(BTBW)+" Control:"+str(BCBW)+" Data:"+str(BDBW))
    print('')
    print('\t\t--->DEV<---')
    print('')
    DTBW, DCBW, DDBW = newget_BwKbTotal(ExpFolder+'/'+ExpJobs, 'dev', NDUtility(ExpFolder+'/'+ExpJobs))
    #print("Dev Total:"+str(DTBW)+" Control:"+str(DCBW)+" Data:"+str(DDBW))
    print('_______________________________')
    print('')
    print('    DATA DIFF:    '+str(BDBW-DDBW))
    print('_______________________________')
    print('*****************************************************************')
    dataDiff.append(BDBW-DDBW)
print('_______________________________')
print('')
print('Avg Data Diff:    '+str((sum(dataDiff, 0.0))/len(dataDiff)))
print(' (Base - Dev)')
print('_______________________________')
