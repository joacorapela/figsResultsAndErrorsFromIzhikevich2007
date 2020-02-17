
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from KirModel import KirModel

def main(argv):
    i0 = 6
    t0 = 0
    v0 = -70
    vf = -20
    dv = .1
    ylim = (-2, 2)

    def i(t): return(i0)
    kirModel = KirModel(i=i)
    vs = np.arange(v0, vf, dv)
    fs = np.empty(len(vs))
    for i in xrange(len(vs)):
        fs[i] = kirModel.deriv(t=t0, v=vs[i])

    plt.plot(vs, fs)
    plt.ylim(ylim)
    plt.ylabel("F(V)")
    plt.xlabel("V")
    plt.grid()
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

