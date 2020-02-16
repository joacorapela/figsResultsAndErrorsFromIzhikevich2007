
import sys
import numpy as np
import matplotlib.pyplot as plt
from ApproxHodgkinAndHuxleyModel import ApproxHodgkinAndHuxleyModel
import pdb

def main(argv):
    ahhModel = ApproxHodgkinAndHuxleyModel(i=None)
    vEqs = np.arange(-20, 120, 1)
    iInfs = ahhModel._gL*(vEqs-ahhModel._eL)+\
             ahhModel._gKMax*pow(ahhModel._nInf(v=vEqs),4)*(vEqs-ahhModel._eK)+\
             ahhModel._gNaMax*pow(ahhModel._mInf(v=vEqs),3)*\
              ahhModel._hInf(v=vEqs)*(vEqs-ahhModel._eNa)

    stableColor = "blue"
    unstableColor = "red"
    stableVEqs = []
    unstableVEqs = []
    stableIInfs = []
    unstableIInfs = []
    for i in xrange(len(vEqs)):
        vEq = vEqs[i]
        iInf = iInfs[i]
        if ahhModel.checkStability(v=vEq)==ahhModel.STABLE:
            stableVEqs.append(vEq)
            stableIInfs.append(iInf)
        else:
            unstableVEqs.append(vEq)
            unstableIInfs.append(iInf)
    stablePlot = plt.scatter(x=stableIInfs, y=stableVEqs, c=stableColor)
    unstablePlot = plt.scatter(x=unstableIInfs, y=unstableVEqs, c=unstableColor)
    plt.legend((stablePlot, unstablePlot), ("Stable", "Unstable"), 
                                           loc="upper left")
    plt.xlabel("I")
    plt.ylabel("V")
    plt.grid()
    # plt.axhline(y=0, color="black")
    # plt.axvline(x=0, color="black")
    plt.show()
    pdb.set_trace()


if __name__=="__main__":
    main(sys.argv)
