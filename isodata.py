import math;
import random;


def isodata(kinit, nmin, imax, dmax, lmininit, pmax, data: list, datadimensions):
    k, centerPoints = isodataInit(kinit, nmin, imax, dmax, lmininit, pmax, data, datadimensions)
    iterations = 0
    global lmin
    lmin = lmininit
    while iterations <= imax:
        clusters = ClusterPoints(k, centerPoints, [[] for c in centerPoints], data)
        clusterRemoved, k = RemoveClusters(k, centerPoints, clusters)
        centerPoints = MoveClusterCenters(k, clusters)
        if clusterRemoved:
            print("Jumping back after removing clusters. Clusters:", (k, len(centerPoints), len(clusters)))
            continue
        delta, deltas = CalcDelta(k, iterations, data, centerPoints, clusters)
        skiptonine = False
        if iterations == imax:
            lmin = 0
            print("Last iteration skipping to Step 9:", (k, len(centerPoints), len(clusters)))
            skiptonine = True
        elif 2 * k > initParams[0] and (iterations % 2 == 0 or k >= 2 * initParams[0]):
            print("Skipping to step 9:", (k, len(centerPoints), len(clusters)))
            skiptonine = True
        if not skiptonine:
            continueloop, k, centerPoints, v = splitclusters(k, iterations, data, centerPoints, clusters, deltas, delta)
            if continueloop:
                print("Jumping back after splitting clusters. Clusters:", (k, len(centerPoints), len(clusters)))
                continue
        distances = interclusterdistance(centerPoints)
        k = mergeclusters(k, distances, clusters, centerPoints)
        print("Iteration over. Clusters:", (k, len(centerPoints), len(clusters)))
        iterations += 1
    return k, centerPoints, clusters





# Algorithm
def isodataInit(kinit, nmin, imax, dmax, lmin, pmax, data: list, datadimensions):
    # Init
    global initParams
    initParams = (kinit, nmin, imax, dmax, lmin, pmax, datadimensions)
    dataWorkingCopy = data.copy()
    random.shuffle(dataWorkingCopy)
    centerPoints = []
    clusters = []
    # Choose Cluster Centers
    for n in range(0, kinit):
        t = tuple(dataWorkingCopy.pop())
        centerPoints.append(t)
        clusters.append([t])
    return kinit, centerPoints
    # ClusterPoints(data, imax, data, centerPoints, clusters, dataWorkingCopy)


def ClusterPoints(centerCount, centerPoints: list, clusters: list, data: list):
    # Cluster points
    for toCluster in data:
        c: int
        d = math.inf
        for n in range(0, centerCount):
            p = centerPoints[n]
            newD = Distance(p, toCluster)
            if newD < d:
                c = n
                d = newD
        clusters[c].append(toCluster)
    return clusters

    # RemoveClusters(centerCount, iterations, data, centerPoints, clusters)


def RemoveClusters(k, clusterPoints : list, clusters: list):
    nmin = initParams[1]
    # Remove small cluster centers
    newK = k
    repeat = False
    for l in range(0, k):
        c = clusters[l]
        p = clusterPoints[l]
        if len(c) < nmin:
            clusters.remove(c)
            clusterPoints.remove(p)
            newK -= 1
            repeat = True
    return repeat, newK
    # MoveClusterCenters(newK, iterations, data, centerPoints, clusters, repeat)


def MoveClusterCenters(k, clusters: list):
    centerPoints = []
    for n in range(0, k):
        c = clusters[n]
        sum = tuple([0 for i in range(0, initParams[6])])
        for t in c:
            sum = Add(sum, t)
        center = Scalar(1/len(c), sum)
        centerPoints.append(center)
    return centerPoints
    # if(repeat):
    #    ClusterPoints(k, iterations, data, centerPoints, clusters, data.copy())
    # CalcDelta(k, iterations, data, centerPoints, clusters)


def CalcDelta(k, iterations, data: set, centerPoints: list, clusters: list):
    deltas = []
    for i in range(0, k):
        c = clusters[i]
        center = centerPoints[i]
        scalar = 1 / len(c)
        deltas.append(scalar * sum([Distance(center, p) for p in c]))
    delta = (1 / len(data)) * sum([len(clusters[i]) * deltas[i] for i in range(0, k)])
    return (delta, deltas)
    # if(iterations == 0):
    #    lmin = 0
    #    #Goto Step 9 TODO
    # if 2*k>initParams[0] and (iterations%2==0 or k>=2*initParams[0]):
    #    pass
    #    #Goto Step 9 TODO


def splitclusters(k, iterations, data: set, centerPoints: list, clusters: list, deltas: list, delta):
    v = []
    for i in range(0, k):
        v.append([])
        for j in range(0, initParams[6]):
            v[i].append(math.sqrt((1 / len(clusters[i])) * sum([(x[j] - centerPoints[i][j]) ** 2 for x in clusters[i]])))
    newCenters = centerPoints.copy()
    newiteration = False
    newK = k
    for i in range(0, k):
        if (max(v[i]) > initParams[3]
                and ((deltas[i] > delta and len(clusters[i]) > 2 * (initParams[1] + 1)) or k <= (initParams[0] / 2))):
            newK += 1
            diff = tuple([max(v[i]) if j == JMax(v[i]) else 0 for j in range(0, initParams[6])])
            zplus = Add(centerPoints[i], diff)
            zminus = Diff(centerPoints[i], diff)
            newCenters.remove(centerPoints[i])
            newCenters.append(zplus)
            newCenters.append(zminus)
            newiteration = True
    return (newiteration, newK, newCenters, v)
    # if newiteration:
    #    ClusterPoints(newK, iterations - 1, data, newCenters, )

def interclusterdistance(centerPoints : list):
    #d = []
    #for c in centerPoints:
    #    distances = []
    #    for z in centerPoints:
    #        distances.append(Distance(c, z))
    #    d.append(distances)
    #return d
    d = set()
    for i in range(0, len(centerPoints)):
        for j in range(i+1, len(centerPoints)):
            d = d | {(Distance(centerPoints[i], centerPoints[j]), i, j)}
    return d

def mergeclusters(k: int, distances : set, clusters : list, centerPoints : list):
    sdistances = sorted(distances,  key=lambda val: val[0])
    tomerge = sdistances[0:min(initParams[5], len(sdistances))]
    merged = set()
    for t in tomerge:
        if t[1] in merged or t[2] in merged or t[0] > lmin:
            continue
        c1 = clusters[t[1]]
        c2 = clusters[t[2]]
        newCluster = c1 + c2
        clusters.remove(c1)
        clusters.remove(c2)
        clusters.append(newCluster)
        p1 = centerPoints[t[1]]
        p2 = centerPoints[t[2]]
        newCenter = Scalar(1/(len(c1)+len(c2)), Add(Scalar(len(c1), p1), Scalar(len(c2), p2)))
        centerPoints.remove(p1)
        centerPoints.remove(p2)
        centerPoints.append(newCenter)
        k -= 1
        merged |= {t[1], t[2]}
    return k

def Distance(a: tuple, b: tuple):
    sum = 0
    for val in Diff(a,b):
        sum += val ** 2
    return math.sqrt(sum)


def JMax(t: list):
    for i in range(0, len(t)):
        if t[i] == max(t):
            return i

def Diff(a : tuple, b : tuple):
    return tuple([a[i]-b[i] for i in range(0,max(len(a),len(b)))])
def Add(a : tuple, b : tuple):
    return tuple([a[i]+b[i] for i in range(0,max(len(a),len(b)))])
def Scalar(a, b : tuple):
    return tuple([a * x for x in b])
def cmpdistance(a : tuple, b : tuple):
    if a[0] > b[0]:
        return 1
    elif a[0] == b[0]:
        return 0
    else:
        return -1
