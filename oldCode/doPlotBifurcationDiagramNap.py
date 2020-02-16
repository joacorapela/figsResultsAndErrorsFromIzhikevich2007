
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from NapModel import NapModel

def main(argv):
    i0 = -100
    v0 = -125
    vf = 40
    dv = 1

    def i(t): return(i0)
    napModel = NapModel(i=i)
    vs = np.arange(v0, vf, dv)
    currents = np.zeros(len(vs))
    for i in xrange(len(vs)):
        currents[i] = napModel.getIInf(v=vs[i])

    plt.plot(currents, vs)
    plt.ylabel(r"$V_{eq}$")
    plt.xlabel("I")
    plt.grid()
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

