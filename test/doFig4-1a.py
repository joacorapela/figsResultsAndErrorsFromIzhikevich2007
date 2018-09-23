

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):
    EL = -80
    gL = 8
    gNa = 20
    gK = 10
    VoneHalf_m = -20
    k_m = 15
    VoneHalf_n = -25
    k_n = 5
    ENa = 60
    EK = -90

    vs = np.arange(-100, 60, 0.01)
    ILs = gL*(vs-EL)
    mInf = 1.0/(1+np.exp((VoneHalf_m-vs)/k_m))
    INaps = gNa*mInf*(vs-ENa)
    nInf = 1.0/(1+np.exp((VoneHalf_n-vs)/k_n))
    IKs = gK*nInf*(vs-EK)
    ITs = ILs+INaps+IKs

    plt.plot(vs, ILs, label="IL")
    plt.plot(vs, INaps, label="INap")
    plt.plot(vs, IKs, label="IK")
    plt.plot(vs, ITs, label="I")
    plt.ylim((-200, 200))
    plt.axhline()
    plt.xlabel("V (mV)")
    plt.ylabel("Current (pA)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main(sys.argv)

