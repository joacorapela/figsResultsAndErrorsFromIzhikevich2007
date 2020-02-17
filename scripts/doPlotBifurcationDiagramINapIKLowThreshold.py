
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel

def main(argv):
    i0 = 0
    # v0 = -70.0
    # vf = -50.0
    v0 = -56.6
    vf = -56.3
    dv = 1e-5
    # xlim = (-100, 100)
    # ylim = (-80, -20)
    markerStableNode = '.'
    markerUnStableNode = '.'
    markerStableFocus = '*'
    markerUnStableFocus = '*'
    markerSaddle = 'o'
    linestyleStableNode = ''
    linestyleUnStableNode = ''
    linestyleStableFocus = ''
    linestyleUnStableFocus = ''
    linestyleSaddle = ''
    figFilename = "figures/bifurcationDiagramINapIKLowThreshold.eps"

    def i(t): return(i0)
    iNapIKModel = INapIKModel.getLowThresholdInstance(i=i)
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
        i = iNapIKModel.getIInf(v=v)
        isAll.append(i)
        stabilityType, lambdas, _ = iNapIKModel.checkStability(v0=v, n0=n)
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

    plt.plot(isStableNode, vsStableNode, marker=markerStableNode,
                           linestyle=linestyleStableNode,
                           label="Stable Node")
    plt.plot(isUnStableNode, vsUnStableNode, marker=markerUnStableNode,
                             linestyle=linestyleUnStableNode,
                             label="UnStable Node")
    plt.plot(isStableFocus, vsStableFocus, marker=markerStableFocus,
                            linestyle=linestyleStableFocus,
                            label="Stable Focus")
    plt.plot(isUnStableFocus, vsUnStableFocus, marker=markerUnStableFocus,
                              linestyle=linestyleUnStableFocus,
                              label="UnStable Focus")
    plt.plot(isSaddle, vsSaddle, marker=markerSaddle,
                       linestyle=linestyleSaddle,
                       label="Saddle")
    # plt.xlim(xlim)
    # plt.ylim(ylim)
    plt.ylabel(r"$V_{eq}$")
    plt.xlabel("I")
    plt.legend()
    plt.grid()
    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

