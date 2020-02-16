
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from KirModel import KirModel

def main(argv):
    i0 = 6
    t0 = 0
    v0 = -68
    vf = -20
    dv = .1

    def i(t): return(i0)
    kirModel = KirModel(i=i)
    vs = np.arange(v0, vf, dv)
    currents = np.zeros(len(vs))
    for i in xrange(len(vs)):
        currents[i] = kirModel.getIInf(v=vs[i])

    plt.plot(currents, vs)
    plt.ylabel(r"$V_{eq}$")
    plt.xlabel("I")
    plt.grid()
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

