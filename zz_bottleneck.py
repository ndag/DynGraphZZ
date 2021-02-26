import dionysus as d
from collections import defaultdict
import sys

def compute_barcodes(filename):
    f = open(filename,'r')

    simplices = defaultdict(list)
    for line in f:
        line = line.strip()
        sline = line.split(",")
        time = float(sline[0])

        if sline[1] == "an" or sline[1] == "dn":
            simplex = (sline[2])
            simple = frozenset([simplex])
            simplices[simple].append(time)
        if sline[1] == "ae" or sline[1] == "de":
            simplex = (sline[2],sline[3])
            simple = frozenset(simplex)
            simplices[simple].append(time)
        if sline[1] == "af" or sline[1] == "df":
            simplex = (sline[2],sline[3],sline[4])
            simple = frozenset(simplex)
            simplices[simple].append(time)

    filtlist = []
    times = []

    for key,value in simplices.items():
        simplex = list(map(int,key))
        filtlist.append(simplex)
        times.append(value)

    filt = d.Filtration(filtlist)
    zz, dgms, cells  = d.zigzag_homology_persistence(filt,times)

    #if you want to print the barcodes in a given dimension:
    #for i in dgms[0]:
    #print(i)

    return dgms


if __name__ == "__main__":
    filename1 = sys.argv[-2]
    filename2 = sys.argv[-1]
    
    dgms1 = compute_barcodes(filename1)
    dgms2 = compute_barcodes(filename2)

    bdist0 = d.bottleneck_distance(dgms1[0],dgms2[0])
    bdist1 = d.bottleneck_distance(dgms1[1],dgms2[1])

    print("0-dimensional bottleneck distance is:")
    print(bdist0)
    print("1-dimensional bottleneck distance is:")
    print(bdist1)
