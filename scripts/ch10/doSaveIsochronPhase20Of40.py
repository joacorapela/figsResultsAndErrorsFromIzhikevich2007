

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import getPeakIndices, computeIsochron

def main(argv):
    # if len(argv)!=3:
        # sys.exit("Usage: %s <phase index> <number of phases>"%argv[0])
    # indexPhaseX0 = int(argv[1])
    # numberOfPhasesForX0 = int(argv[2])
    indexPhaseX0 = 20
    numberOfPhasesForX0 = 40
    i0 = 10
    # factorsDeltaT = 1.0/12.0*np.arange(1, 11)
    factorsDeltaT = 1.0/12.0*np.arange(4, 5)
    # factorsDeltaT = 1.0/32.0*np.arange(1, 6)
    # factorsDeltaT = 1.0/32.0*np.arange(5, 6)
    nInitialConditions = 20
    # maxDeltaX0 = 1.0
    # maxDeltaX1 = 0.01
    maxDistance = 0.01
    dt = 1e-5
    vMin = -50.0
    vMax = -20.0
    tol=1e-3
    addIntersectNullclines = False
    integrationFilename = "results/integrationINapIKFig10_1.npz"
    isochronFilename = \
     "results/isochronINapIKFig10_1Phase%02dOver%d.npz"%(indexPhaseX0, 
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

    def i(t):
        return(i0)
    model = INapIKModel.getHighThresholdInstance(i=i)
    print("Processing x0=(%.2f,%.4f)"%(x0[0], x0[1]))
    plt.annotate("x0", xy=x0, color="red", size=14)
#     isochron = computeIsochron(model, x0=x0, deltaTs=factorsDeltaT*period, nInitialConditions=nInitialConditions, maxDeltaX0=maxDeltaX0, maxDeltaX1=maxDeltaX1, dt=dt)
    isochron = computeIsochron(model, x0=x0, deltaTs=factorsDeltaT*period, nInitialConditions=nInitialConditions, maxDistance=maxDistance, dt=dt)
    if addIntersectNullclines:
        xIntersectionNullclines = model.getIntersectionOfNullclines(vMin=vMin,
                                                                     vMax=vMax,
                                                                     tol=tol)
        isochron = np.append(xIntersectionNullclines, isochron, 1)
    # plt.show()
    np.savez(isochronFilename, isochron=isochron)

if __name__ == "__main__":
    main(sys.argv)

