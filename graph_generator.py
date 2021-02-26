import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import sys

def get_numlines(infile):
    file = open(infile,"r")
    counter = 0

    content = file.read()
    colist = content.split("\n")

    for i in colist:
        if i:
            counter += 1
    file.close()
    
    return counter


def get_points(file, numpts):
    points = []
    for i in range(numpts):
        line = file.readline()
        sline = line.split(' ')
        fline = list(map(float, sline))
        points.append(fline)
    return np.array(points)


def get_dist(distmat, key, epsilon):
    if len(key)==1:
        return 'y'
    if len(key)==2:     
        dist = distmat[key[0],key[1]] 
        if dist < epsilon:
            return 'y'
        else:
            return 'n'
    if len(key)==3:
        dist1 = distmat[key[0],key[1]]
        dist2 = distmat[key[0],key[2]]
        dist3 = distmat[key[1],key[2]]
        if dist1 < epsilon and dist2 < epsilon and dist3 < epsilon:
            return 'y'
        else:
            return 'n'


def generate_graph(infile, outfile, numpts, threshold):
    numlines = get_numlines(infile)
    time_periods = int(numlines/numpts)

    keys = []
    for i in range(numpts):
        keys.append( (i,))

    for i in range(numpts):
        for j in range(int(i)+1,numpts):
            keys.append((i,j))

    for i in range(numpts):
        for j in range(int(i)+1,numpts):
            for k in range(int(j)+1,numpts):
                keys.append((i,j,k))

    simplices = dict.fromkeys(keys)
    simplices2 = dict.fromkeys(keys)
    for key in simplices:
        simplices[key] = []
    
    f = open(infile)

    dists = []
    for i in range(time_periods):
        temppts = get_points(f,numpts)
        dists.append(squareform(pdist(temppts)))

    for time in dists:
        for key in simplices:
            truth = get_dist(time, key, threshold)
            simplices[key].append(truth)

    f.close()

    fileid = open(outfile,"w")
    for key in simplices:
        if len(key) == 1:
            fileid.write('0,an,'+','.join(map(str,key))+'\n')
        if len(key) == 2 and simplices[key][0] == 'y':
            fileid.write('0,ae,'+','.join(map(str,key))+'\n')
        if len(key) == 3 and simplices[key][0] == 'y':
            fileid.write('0,af,'+','.join(map(str,key))+'\n')

    for time in range(1,time_periods):
        for key in simplices:
            y = int(time)
            if simplices[key][y] == 'n' and simplices[key][y-1] == 'y':
                if len(key) == 2:
                    fileid.write(str(y)+',de,'+','.join(map(str,key))+'\n')
                if len(key) == 3:
                    fileid.write(str(y)+',df,'+','.join(map(str,key))+'\n')
            if simplices[key][y] == 'y' and simplices[key][y-1] == 'n':
                if len(key) == 2:
                    fileid.write(str(y)+',ae,'+','.join(map(str,key))+'\n')
                if len(key) == 3:
                    fileid.write(str(y)+',af,'+','.join(map(str,key))+'\n')

    for key in simplices:
        if simplices[key][-1] == 'y':
            if len(key) == 1:
                fileid.write(str(time_periods)+',dn,'+','.join(map(str,key))+'\n')
            if len(key) == 2:
                fileid.write(str(time_periods)+',de,'+','.join(map(str,key))+'\n')
            if len(key) == 3:
                fileid.write(str(time_periods)+',df,'+','.join(map(str,key))+'\n')

    fileid.close()


if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    numpts = int(sys.argv[3])
    threshold = float(sys.argv[4])
    
    generate_graph(infile, outfile, numpts, threshold)

