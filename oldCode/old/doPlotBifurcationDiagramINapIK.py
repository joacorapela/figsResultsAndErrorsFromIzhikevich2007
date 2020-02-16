
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel

def main(argv):
    i0 = 0
    v0 = -80.0
    vf = -20.0
    dv = 1e-4
    xlim = (-100, 100)
    ylim = (-80, -20)

    def i(t): return(i0)
    iNapIKModel = INapIKModel.getHighThresholdInstance(i=i)
    vs = np.arange(v0, vf, dv)
    vsStableNode = []
    vsUnStableNode = []
    vsStableFocus = []
    vsUnStableFocus = []
    vsSaddle = []
    isStableNode = []
    isUnStableNode = []
    isStableFocus = []
    isUnStableFocus = []
    isSaddle = []
    lambdasCol = np.empty([len(vs),2])
    isAll = []
    for j in xrange(len(vs)):
        v = vs[j]
        n = iNapIKModel._nInf(v=vs[j])
        i = iNapIKModel.getIInf(y=(v, n))
        isAll.append(i)
        stabilityType, lambdas = iNapIKModel.checkStability(i0=i, v0=v, n0=n)
        lambdasCol[j,:] = lambdas
        if stabilityType==iNapIKModel.STABLE_NODE:
            vsStableNode.append(v)
            isStableNode.append(i)
        elif stabilityType==iNapIKModel.UNSTABLE_NODE:
            vsUnStableNode.append(v)
            isUnStableNode.append(i)
        elif stabilityType==iNapIKModel.STABLE_FOCUS:
            vsStableFocus.append(v)
            isStableFocus.append(i)
        elif stabilityType==iNapIKModel.UNSTABLE_FOCUS:
            vsUnStableFocus.append(v)
            isUnStableFocus.append(i)
        elif stabilityType==iNapIKModel.SADDLE:
            vsSaddle.append(v)
            isSaddle.append(i)
        else: raise RuntimeError("Invalid stabilityType (%d)"%(stabilityType))

    plt.plot(isStableNode, vsStableNode, label="Stable Node")
    plt.plot(isUnStableNode, vsUnStableNode, label="UnStable Node")
    plt.plot(isStableFocus, vsStableFocus, label="Stable Focus")
    plt.plot(isUnStableFocus, vsUnStableFocus, label="UnStable Focus")
    plt.plot(isSaddle, vsSaddle, label="Saddle")
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.ylabel(r"$V_{eq}$")
    plt.xlabel("I")
    plt.legend()
    plt.grid()
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

