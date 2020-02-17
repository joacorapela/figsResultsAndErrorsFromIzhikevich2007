
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from NapModel import NapModel

def main(argv):
    i0 = -100
    t0 = 0
    v0 = -100
    vf = 50
    dv = 1

    def i(t): return(i0)
    napModel = NapModel(i=i)
    vs = range(v0, vf, dv)
    fs = np.empty(len(vs))
    for i in xrange(len(vs)):
        fs[i] = napModel.deriv(t=t0, v=vs[i])

    plt.plot(vs, fs)
    plt.ylabel("F(V)")
    plt.xlabel("V")
    plt.grid()
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

