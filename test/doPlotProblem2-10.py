
import sys
import numpy as np
import matplotlib.pyplot as plt
from HodkingHuxleyModel import HodkingHuxleyModel
import pdb

def main(argv):
    vEqs = np.arange(-65, -20, .5)
    hhModel = HodkingHuxleyModel(i=None)
    iInfs = hhModel.getIInf(v=vEqs)
    stableColor = "blue"
    unstableColor = "red"
    stableVEqs = []
    unstableVEqs = []
    stableIInfs = []
    unstableIInfs = []
    for i in xrange(len(vEqs)):
        vEq = vEqs[i]
        iInf = iInfs[i]
        if hhModel.checkStability(v=vEq)==hhModel.STABLE:
            stableVEqs.append(vEq)
            stableIInfs.append(iInf)
        else:
            unstableVEqs.append(vEq)
            unstableIInfs.append(iInf)
    stablePlot = plt.scatter(x=stableIInfs, y=stableVEqs, c=stableColor)
    unstablePlot = plt.scatter(x=unstableIInfs, y=unstableVEqs, c=unstableColor)
    plt.legend((stablePlot, unstablePlot), ("Stable", "Unstable"))
    plt.xlabel("I")
    plt.ylabel("V")
    plt.grid()
    # plt.axhline(y=0, color="black")
    # plt.axvline(x=0, color="black")
    plt.show()

if __name__=="__main__":
    main(sys.argv)
