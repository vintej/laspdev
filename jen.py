from jenks import jenks
import numpy as np
import random
import NDutility as ND

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

if __name__=="__main__":
    gvf = 0.0
    nclasses = 3
    print (ND.get_allNodes())
    print ('NodeLength:'+str(len(ND.get_allNodes())))
    '''randar =  np.random.randint(1,100,8)
    print(np.sort(randar))
    while gvf < .9 and nclasses!=2:
        gvf = goodness_of_variance_fit(randar, nclasses)
        print(np.sort(randar))
        print("GVF: "+str(gvf))
        print nclasses
        print(jenks(randar,nclasses))
        nclasses += 1
        if nclasses > 3:
            nclasses = 3
            randar =  np.random.randint(1,100,8)'''
    #a = np.array([2,2, 4, 20, 18, 22, 28, 35, 42])
    #a = np.array([1, 2, 10, 8, 0, 5, 6, 0, 10, 8, 49, 40, 49, 46, 30, 42, 39, 46, 44, 33, 32, 34, 37, 30, 39, 33, 39, 46, 32, 37, 46, 43, 49, 39, 50, 50, 50, 34, 38, 49, 34, 44, 39, 36, 32, 39, 40, 48, 49, 39, 35, 47, 43, 39, 50, 30, 37, 46, 50, 31, 45, 45, 38, 32, 33, 30, 32, 47, 47, 42, 42, 48, 44, 44, 31, 50, 38, 39, 50, 33, 37, 36, 50, 44, 31, 34, 50, 47, 30, 44, 78, 74, 73, 77, 62, 67, 70, 66, 64, 65, 72, 65, 83, 66, 69, 60, 62, 85, 80, 65])
    a = np.array([8, 10, 7, 11, 9, 6, 10, 8, 9, 10, 36, 39, 38, 42, 35, 37, 47, 41, 46, 38, 32, 48, 42, 38, 43, 33, 40, 41, 45, 37, 36, 41, 30, 43, 48, 49, 36, 50, 45, 32, 35, 34, 36, 48, 31, 33, 38, 49, 50, 48, 34, 33, 36, 36, 40, 49, 32, 34, 45, 48, 49, 46, 47, 50, 33, 49, 40, 48, 49, 33, 88, 70, 79, 63, 86, 60, 83, 75, 88, 60, 77, 62, 65, 73, 72, 64, 62, 66, 76, 71, 75, 63, 66, 60, 85, 65, 61, 62, 69, 75])
    #a =  np.random.randint(1,100,8)
    gvf = goodness_of_variance_fit(a, 3)
    print(np.sort(a))
    print("GVF: "+str(gvf))
    segs = jenks(a,3)
    print("SEGS:"+str(segs))
    rates = np.sort(a).tolist()
    peers = ['d1', 'd2' , 'd3', 'd4', 'd5', 'd6', 'd7', 'd8']
    c1 = {}
    c2 = {}
    c3 = {}
    c1_rates = []
    c2_rates = []
    c3_rates = []
    random.shuffle(peers)
    print(peers)
    print("NP SORT"+str(np.sort(a)))
    ind = 0
    for i in rates:
        if i <= segs[1]:
            c1_rates.append(i)
    #        c1.update({peers[ind] : i})
        elif i <= segs[2]:
            c2_rates.append(i)
    #        c2.update({peers[ind] : i})
        elif i <= segs[3]:
            c3_rates.append(i)
    #        c3.update({peers[ind] : i})
    #    ind += 1
    #sort_rate = {'c1' : {}, 'c2' : {}, 'c3' : {}}
    #sort_rate.update({'c1' : c1})
    ##sort_rate.update({'c2' : c2})
    #sort_rate.update({'c3' : c3})
    #print sort_rate
    print("C1:"+str(c1_rates)+" Len:"+str(len(c1_rates)))
    print("C2:"+str(c2_rates)+" Len:"+str(len(c2_rates)))
    print("C3:"+str(c3_rates)+" Len:"+str(len(c3_rates)))
    
