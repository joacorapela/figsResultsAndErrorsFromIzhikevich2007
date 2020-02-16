

import sys
import numpy as np
import math
from scipy.interpolate import splprep, splev
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import getPeakIndices, computeIsochron, sortIsochron
from plotFunctions import plotINapIKNullclines

def main(argv):
    indexPhaseX0 = 7
    numberOfPhasesForX0 = 40
    i0 = 10
    nSPLUNew = 1000
    vMin = -90
    vMax = 15
    nMin = -0.1
    nMax = 0.8
    integrationFilename = "results/integrationINapIKFig10_1.npz"
    isochronFilename = \
     "results/isochronINapIKFig10_1Phase%02dOver%d.npz"%(indexPhaseX0, 
                                                        numberOfPhasesForX0)
    figFilename = \
     "figures/isochronINapIKFig10_1Phase%02dOver%d.eps"%(indexPhaseX0, 
                                                        numberOfPhasesForX0)

    results = np.load(integrationFilename)
    times = results["times"]
    ys = results["ys"]
    spikeIndices = getPeakIndices(v=ys[0,:])
    spikeTimes = times[spikeIndices]

    times = np.delete(times, np.arange(0,spikeIndices[0]))
    times = times-times[0]
    ys = np.delete(ys, np.arange(0,spikeIndices[0]), axis=1)
    spikeIndices = spikeIndices-spikeIndices[0]
    spikeTimes = spikeTimes-spikeTimes[0]
    period = spikeTimes[1]-spikeTimes[0]
    phases = times%period
    phasesForX0 = np.arange(0, period, period/numberOfPhasesForX0)
    indicesBtwFirstAndSecondSpike = np.arange(0, spikeIndices[1])
    phasesToSearch = phases[indicesBtwFirstAndSecondSpike]

    indicesPhasesForX0 = np.empty(len(phasesForX0), dtype=np.int64)
    for i in xrange(len(phasesForX0)):
        phaseForX0 = phasesForX0[i]
        indicesPhasesForX0[i] = np.argmin(np.abs(phasesToSearch-phaseForX0))
    x0 = ys[:, indicesPhasesForX0[indexPhaseX0]]

    results = np.load(isochronFilename)
    isochron = results["isochron"]

    validIndices = np.logical_and(np.logical_and(vMin<=isochron[0,:], 
                                                  isochron[0,:]<=vMax),
                                   np.logical_and(nMin<=isochron[1,:], 
                                                   isochron[1,:]<=nMax)).nonzero()[0]
    isochron = isochron[:,validIndices]

    sortedIsochron = sortIsochron(isochron=isochron)

    splTck, splU = splprep(sortedIsochron, s=5.0)
    splUNew = np.linspace(splU.min(), splU.max(), nSPLUNew)
    splXInter, splYInter = splev(splUNew, splTck, der=0)

    # plt.figure()
    # plotHighThresholdINapIKVectorField(i=i0)
    plt.plot(ys[0, :], ys[1, :], label="limit cycle attractor")
    # pdb.set_trace()

    plt.annotate("x0", xy=x0, color="red", size=14)

    def i(t):
        return(i0)
    model = INapIKModel.getHighThresholdInstance(i=i)
    plotINapIKNullclines(i=i0, eL=model._eL, gL=model._gL, eNa=model._eNa, gNa=model._gNa, eK=model._eK, gK=model._gK, mVOneHalf=model._mVOneHalf, mK=model._mK, nVOneHalf=model._nVOneHalf, nK=model._nK)
    plt.plot(isochron[0,:], isochron[1,:], marker="o", color="red", linestyle="None")
    plt.plot(splXInter, splYInter, color="gray", linestyle="solid")
    plt.legend(loc="upper left")
    plt.xlabel("Voltage (mv)")
    plt.ylabel("K activation variable, n")
    plt.xlim((-90, 15))
    plt.ylim((-0.1, 0.8))
    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

