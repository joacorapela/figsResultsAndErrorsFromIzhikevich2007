
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from QuadraticIFModel import QuadraticIFModel

def main(argv):
    i0 = 7.0
    vSN = -60.9325
    t0 = 0.0
    tf = 15.0
    dt = 1e-3
    resultsFilename = 'results/quadraticIFSolutions.npz'

    qifModel = QuadraticIFModel(i=i0, iSN=4.51, vSN=vSN, a=0.1887, c=1.0, 
                                      vReset=-80.0, vMax=-30.0)
    times, vs = qifModel.getSolution(v0=vSN, t0=t0, tf=tf, srate=1.0/dt)
    np.savez(resultsFilename, times=times, vs=vs)
    pdb.set_trace()

    plt.plot(times, vs)
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Voltage (mV)")
    plt.show()

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
