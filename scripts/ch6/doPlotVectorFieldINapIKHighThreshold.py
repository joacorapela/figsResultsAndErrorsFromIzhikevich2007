

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from plotFunctions import plotINapIKVectorField

def main(argv):
    figFilename = 'figures/iNapIKHighThresholdVectorField.eps'
    iNapIKModel = INapIKModel.getHighThresholdInstance(i=None)
    i=-10

    plt.figure()
    plotINapIKVectorField(i=i, c=iNapIKModel._c, eL=iNapIKModel._eL,
                               gL=iNapIKModel._gL, gNa=iNapIKModel._gNa,
                               gK=iNapIKModel._gK,
                               mVOneHalf=iNapIKModel._mVOneHalf,
                               mK=iNapIKModel._mK,
                               nVOneHalf=iNapIKModel._nVOneHalf,
                               nK=iNapIKModel._nK, tauV=iNapIKModel._tau(v=0),
                               eNa=iNapIKModel._eNa, eK=iNapIKModel._eK,
                               nDotScaleFactor=200, vMin=-90.0, vMax=20.0,
                               nVs=19, nVsDense=100, nMin=0.0, nMax=0.7,
                               nNs=18, vNullclineLabel="v nullcline",
                               nNullclineLabel="n nullcline")

    plt.savefig(figFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

