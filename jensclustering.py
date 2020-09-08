from jenks import jenks
from threading import Thread
import numpy as np
import random
import NDutility as ND
import time
import pickle
import sys


found = False
gc1_rates = []
gc2_rates = []
gc3_rates = []
c1_peerId = ['c']
c3_peerId = ['d']
    

def goodness_of_variance_fit(array, classes):
    # get the break points
    classes = jenks(array, classes)

    # do the actual classification
    classified = np.array([classify(i, classes) for i in array])

    # max value of zones
    maxz = max(classified)

    # nested list of zone indices
    zone_indices = [[idx for idx, val in enumerate(classified) if zone + 1 == val] for zone in range(maxz)]

    # sum of squared deviations from array mean
    sdam = np.sum((array - array.mean()) ** 2)

    # sorted polygon stats
    array_sort = [np.array([array[index] for index in zone]) for zone in zone_indices]

    # sum of squared deviations of class means
    sdcm = sum([np.sum((classified - classified.mean()) ** 2) for classified in array_sort])

    # goodness of variance fit
    gvf = (sdam - sdcm) / sdam

    return gvf

def classify(value, breaks):
    for i in range(1, len(breaks)):
        if value < breaks[i]:
            return i
    return len(breaks) - 1

def gen_list_gvf(classes):
    gvf = 0.0
    nclasses = classes
    #global c1_peerId, c3_peerId
    
    randar1 =  np.random.randint(1,5,len(c1_peerId))
    randar3 =  np.random.randint(75,100,len(c3_peerId))
    randar2 = np.random.randint(30,50,len(ND.get_allNodes())-len(c3_peerId)-len(c1_peerId))
    randartemp = []
    randartemp.append(randar1)
    randartemp.append(randar2)
    randartemp.append(randar3)
    randar = np.concatenate((randar1, randar2, randar3))
    #randar = randar1 + randar2 + randar3
    #print (randar)
    print(np.sort(randar))
    segs = []
    arr = []
    global found
    while gvf < .5 and nclasses!=2:
        gvf = goodness_of_variance_fit(randar, nclasses)
        print("RandIntegers:"+str(np.sort(randar)))
        print("GVF: "+str(gvf))
        print nclasses
        print(jenks(randar,nclasses))
        segs = jenks(randar,nclasses)
        arr = randar
        nclasses += 1
        if nclasses > 3:
            print ("Randoming randar")
            nclasses = 3
            randar1 =  np.random.randint(1,5,len(c1_peerId))
            randar3 =  np.random.randint(75,100,len(c3_peerId))
            randar2 = np.random.randint(30,50,len(ND.get_allNodes())-len(c3_peerId)-len(c1_peerId))
            randartemp = []
            randartemp.append(randar1)
            randartemp.append(randar2)
            randartemp.append(randar3)
            randar = np.concatenate((randar1, randar2, randar3))
            #randar = np.asarray(randartemp)
            #randar = randar1 + randar2 + randar3
            #randar =  np.random.randint(1,100,len(ND.get_allNodes()))
        print ("New Randar"+str(randar))
        print ("New Randar1"+str(randar1))
        print ("New Randar2"+str(randar2))
        print ("New Randar3"+str(randar3))
        
        
    return segs, arr, gvf

def get_classes():
    gvf = 0.0
    nclasses = 3
    segs, arr, gvf = gen_list_gvf(nclasses)
    print "Got segs:"+str(segs)
    print "Got arr:"+str(np.sort(arr))
    '''

    print ('NodeLength:'+str(len(ND.get_allNodes())))
    #a = np.array([2, 4, 20, 18, 22, 28, 35, 42])
    a =  np.random.randint(1,100,len(ND.get_allNodes()))
    gvf = goodness_of_variance_fit(a, 3)
    print(np.sort(a))
    segs = jenks(a,3)'''
    print("GVF: "+str(gvf))
    print("Segments:"+str(segs))
    rates = arr
    print("Rates:"+str(rates))
    c1_rates = []
    c2_rates = []
    c3_rates = []
    ind = 0
    for i in rates:
        if i <= segs[1]:
            c1_rates.append(i)
        elif i <= segs[2]:
            c2_rates.append(i)
        elif i <= segs[3]:
            c3_rates.append(i)
        ind += 1
    print c1_rates
    print c2_rates
    print c3_rates
    return c1_rates, c2_rates, c3_rates

def find_rates(c1_peerId, c3_peerId):
    global found
    c1_rates = []
    c2_rates = []
    c3_rates = []
    i = 0
    while found == False:
        c1_rates, c2_rates, c3_rates = get_classes()
        if len(c1_rates)==len(c1_peerId) and len(c3_rates) == len(c3_peerId):
            print ("Length of c1_rates"+str(len(c1_rates)))
            print ("Length of c3_rates"+str(len(c3_rates)))
            found = True
            global gc1_rates, gc2_rates, gc3_rates
            gc1_rates = c1_rates
            gc2_rates = c2_rates
            gc3_rates = c3_rates
            print "GC1"+str(gc1_rates)
            print "GC2"+str(gc2_rates)
            print "GC3"+str(gc3_rates)
            found = True
            break
        found = True
    print ("Finished")
    print "Rates for C1"+str(c1_rates) +" Length of C1:"+str(len(c1_rates))+ " Length of c1_peer" + str(len(c1_peerId))
    print c2_rates
    print "Rates for C3"+str(c3_rates) + "Length of C3:"+str(len(c3_rates))+" Length of c3_peer"+str(len(c3_peerId))
    return c1_rates, c2_rates, c3_rates

def generate_rateclass():
    #global c1_peerId, c3_peerId
    #find_rates(c1_peerId, c3_peerId)
    threads_main = []
    for i in range(1, 2):
        threads_main.append(Thread(target=find_rates, args=(c1_peerId, c3_peerId)))
        threads_main[-1].start()
    #for thread in threads_main:
    #    thread.terminate()
    time.sleep(5)
    print "GC1"+str(gc1_rates)
    print "GC2"+str(gc2_rates)
    print "GC3"+str(gc3_rates)
    rates_final = {}
    rates_final['c1'] = gc1_rates
    rates_final['c2'] = gc2_rates
    rates_final['c3'] = gc3_rates
    with open("Rates.txt", 'wb') as fp:
            pickle.dump(rates_final, fp)
    '''
    peers = ND.get_allNodes()#['d1', 'd2' , 'd3', 'd4', 'd5', 'd6', 'd7', 'd8']
    c1 = {}
    c2 = {}
    c3 = {}
    random.shuffle(peers)
    print(peers)
    c1_peerId = ['c']
    c3_peerId = ['d']
    #print(np.sort(a))
    ind = 0
    temp_rates = rates[:]
    temp_peers = peers[:]
    temp_segs = segs[:]
    tempC1list = []
    tempC2list = []
    tempC3list = []
    c1_rates = []
    c2_rates = []
    c3_rates = []
    for peer in temp_peers:
        temp_rate = temp_rates.pop(0)
        if ND.get_id(peer) in c1_peerId and temp_rate <= temp_segs[1]:
            print(str(peer)+":"+str(temp_rate)+" nodeId:"+str(ND.get_id(peer)))
            tempC1list.append(peer)
        elif ND.get_id(peer) in c3_peerId and temp_rate <= temp_segs[3]:
            print(str(peer)+":"+str(temp_rate)+" nodeId:"+str(ND.get_id(peer)))
            tempC3list.append(peer)
        else:
            print(str(peer)+":"+str(temp_rate)+" nodeId:"+str(ND.get_id(peer)))
            tempC2list.append(peer)
        print "Temp_rates now:"+str(temp_rates)
    print ("Rates:"+str(rates))
    for i in rates:
        if i <= segs[1]:
            print("c1.update({"+str(peers[ind])+":"+str(i))
            c1.update({peers[ind] : i})
            c1_rates.append(i)
        elif i <= segs[2]:
            print("c2.update({"+str(peers[ind])+":"+str(i))
            c2.update({peers[ind] : i})
            c2_rates.append(i)
        elif i <= segs[3]:
            print("c3.update({"+str(peers[ind])+":"+str(i))
            c3.update({peers[ind] : i})
            c3_rates.append(i)
        ind += 1
    sort_rate = {'c1' : {}, 'c2' : {}, 'c3' : {}}
    sort_rate.update({'c1' : c1})
    sort_rate.update({'c2' : c2})
    sort_rate.update({'c3' : c3})
    print ("TempRateLists")
    print tempC1list
    print c1_rates
    print tempC2list
    print c2_rates
    print tempC3list
    print c3_rates
    print ('TempRateLists Done')
    print sort_rate
    '''
if __name__=="__main__":
    operation = sys.argv[1]
    if operation == "start":
        generate_rateclass()
    elif operation == "view":
        with open("Rates.txt", "rb") as fp:
            rates = pickle.load(fp)
        print rates.keys.sort()
        c1avg = 0
        c2avg = 0
        c3avg = 0
        for rate in rates:
            for r in rates[rate]:
                if rate == 'c1':
                    c1avg = c1avg + r
                elif rate == 'c2':
                    c2avg = c2avg + r
                elif rate == 'c3':
                    c3avg = c3avg + r
        print c1avg/len(rates['c1'])
        print c2avg/len(rates['c2'])
        print c3avg/len(rates['c3'])
