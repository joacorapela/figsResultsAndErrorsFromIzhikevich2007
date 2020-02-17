
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INatModel import INatModel

def main(argv):
    i0Dummy = 0
    v0 = -70.0
    vf =  -20.0
    dv = 0.01
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
    figFilename = "figures/bifurcationDiagramINatLowThreshold.eps"

    def iDummy(t): return(i0Dummy)
    iNatModel = INatModel.getLowThresholdInstance(i=iDummy)
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
    for j in xrange(len(vs)):
        v = vs[j]
        h = iNatModel._hInf(v=vs[j])
        i = iNatModel.getIInf(y=[v,h])
        stabilityType, _ = iNatModel.checkStability(i0=i, v0=v, h0=h)
        if stabilityType==iNatModel.STABLE_NODE:
            vsStableNode.append(v)
            isStableNode.append(i)
        elif stabilityType==iNatModel.UNSTABLE_NODE:
            vsUnStableNode.append(v)
            isUnStableNode.append(i)
        elif stabilityType==iNatModel.STABLE_FOCUS:
            vsStableFocus.append(v)
            isStableFocus.append(i)
        elif stabilityType==iNatModel.UNSTABLE_FOCUS:
            vsUnStableFocus.append(v)
            isUnStableFocus.append(i)
        elif stabilityType==iNatModel.SADDLE:
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

