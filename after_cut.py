#!/bin/python
import sys

def afterCut(fileName):
    fh = open(fileName, 'r')
    molecule = dict();
    for line in fh: 
        #fh.seek(0)   
        if line.startswith("@"):
            line = line.rstrip()
            line1 = fh.readline().rstrip()
            line2 = fh.readline().rstrip()
            line3 = fh.readline().rstrip()
            #print(line2)
            temp = line1.split('\t')
            if len(temp) > 1 and len(temp[0]) > 0 and len(temp[1]) >= 12:
                if temp[0]+"_"+temp[1][:12] not in molecule:
                    molecule[temp[0]+"_"+temp[1][:12]] = None;
                    print(line+":"+temp[1][:12])
                    print(temp[0])
                    print(line2)
                    print(line3[:len(temp[0])])
    fh.close()      

if __name__ == "__main__":
    afterCut(sys.argv[1])
