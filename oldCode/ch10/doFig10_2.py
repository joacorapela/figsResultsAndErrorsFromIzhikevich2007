

import sys
import numpy as np
import pdb
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import getPeakIndices, computeIsochron
from plotFunctions import plotINapIKNullclines

def main(argv):
    i0 = 10
    numberOfPhasesForX0 = 40
    indexPhaseX0 = 38
    annotationGap = 0.02
    factorsDeltaT = 1.0/32.0*np.arange(1, 6)
    # factorsDeltaT = 1.0/32.0*np.arange(5, 6)
    nInitialConditions = 10
    maxDeltaX0 = 1.0
    maxDeltaX1 = 0.01
    dt = 1e-5
    nSPLUNew = 1000
    vMin = -90
    vMax = 15
    nMin = -0.1
    nMax = 0.8
    resultsFilename = "results/integrationINapIKFig10_1.npz"
    aFigFilename = "figures/fig10_1b.eps"

    results = np.load(resultsFilename)
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

    def i(t):
        return(i0)
    model = INapIKModel.getHighThresholdInstance(i=i)
    isochron = computeIsochron(model, x0=x0, deltaTs=factorsDeltaT*period, nInitialConditions=nInitialConditions, maxDeltaX0=maxDeltaX0, maxDeltaX1=maxDeltaX1, dt=dt)
    # begin tmp code
    np.savez("~/tmp/isochron.npz", isochron=isochron)
    # results = np.load("/tmp/isochron.npz")
    # isochron = results["isochron"]
    # end tmp code

    validIndices = np.logical_and(np.logical_and(vMin<=isochron[0,:], 
                                                  isochron[0,:]<=vMax),
                                   np.logical_and(nMin<=isochron[1,:], 
                                                   isochron[1,:]<=nMax)).nonzero()[0]
    isochron = isochron[:,validIndices]
    sortOrder = np.argsort(isochron[1,:])
    isochron = isochron[:,sortOrder]
    splTck, splU = splprep(isochron, s=5.0)
    splUNew = np.linspace(splU.min(), splU.max(), nSPLUNew)
    splXInter, splYInter = splev(splUNew, splTck, der=0)

    # plt.figure()
    # plotHighThresholdINapIKVectorField(i=i0)
    plt.plot(ys[0, :], ys[1, :], label="limit cycle attractor")
    # pdb.set_trace()

    plt.annotate("x0", xy=x0, color="red", size=14)

    plotINapIKNullclines(i=i0, eL=model._eL, gL=model._gL, eNa=model._eNa, gNa=model._gNa, eK=model._eK, gK=model._gK, mVOneHalf=model._mVOneHalf, mK=model._mK, nVOneHalf=model._nVOneHalf, nK=model._nK)
    plt.plot(isochron[0,:], isochron[1,:], marker="o", color="red", linestyle="None")
    plt.plot(splXInter, splYInter, color="gray", linestyle="solid")
    plt.legend(loc="upper left")
    plt.xlabel("Voltage (mv)")
    plt.ylabel("K activation variable, n")
    plt.xlim((-90, 15))
    plt.ylim((-0.1, 0.8))
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

