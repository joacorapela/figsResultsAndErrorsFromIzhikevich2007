
import sys
import numpy as np
from QuadraticIFModel import QuadraticIFModel

def main(argv):
    if len(argv)!=2:
        sys.exit("Usage: %s i0"%argv[0])
    i0 = float(argv[1])
    iSN = 4.51
    vSN = -60.9325
    a = 0.1887
    c = 1.0
    spikeDuration = 5.1
    t0 = 0.0
    tf = 100.0
    dt = 1e-2
    vReset = -77
    vMax = 10
    resultsFilename = 'results/quadraticIFSolutionI%.02f.npz'%i0

    qifModel = QuadraticIFModel(i=i0, iSN=iSN, vSN=vSN, a=a, c=c, 
                                      vReset=vReset, vMax=vMax, 
                                      spikeDuration=spikeDuration)
    times, vs = qifModel.getSolution(v0=vSN, t0=t0, tf=tf, srate=1.0/dt)
    np.savez(resultsFilename, times=times, vs=vs)

if __name__=="__main__":
    main(sys.argv)
