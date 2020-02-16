

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField
from utils import getPeakIndices

def main(argv):
    i0 = 35
    numberOfPhaseMarks = 8
    annotationGap = 0.02
    initialTransientLength = 10
    resultsFilename = 'results/integrationINapIKFig10_1_INapIKLowThreshold.npz'
    aFigFilename = 'figures/fig10_1b_INapIKLowThreshold.eps'

    results = np.load(resultsFilename)
    times = results['times']
    ys = results['ys']
    transientIndices = np.nonzero(times<initialTransientLength)[0]
    pdb.set_trace()
    times = np.delete(arr=times, obj=transientIndices)
    ys = np.delete(arr=ys, obj=transientIndices, axis=1)
    spikeIndices = getPeakIndices(v=ys[0,:])
    spikeTimes = times[spikeIndices]

    times = np.delete(times, np.arange(0,spikeIndices[0]))
    times = times-times[0]
    ys = np.delete(ys, np.arange(0,spikeIndices[0]), axis=1)
    spikeIndices = spikeIndices-spikeIndices[0]
    spikeTimes = spikeTimes-spikeTimes[0]
    period = spikeTimes[1]-spikeTimes[0]
    phases = times%period
    phasesToPlot = np.arange(0, period, period/numberOfPhaseMarks)
    indicesBtwFirstAndSecondSpike = np.arange(0, spikeIndices[1])
    phasesToSearch = phases[indicesBtwFirstAndSecondSpike]

    indicesPhasesToPlot = np.empty(len(phasesToPlot), dtype=np.int64)
    for i in xrange(len(phasesToPlot)):
        phaseToPlot = phasesToPlot[i]
        indicesPhasesToPlot[i] = np.argmin(np.abs(phasesToSearch-phaseToPlot))

    plt.figure()
    plotLowThresholdINapIKVectorField(i=i0)
    plt.plot(ys[0, :], ys[1, :], label="limit cycle attractor")
    plt.plot(ys[0, indicesPhasesToPlot], ys[1, indicesPhasesToPlot], 'ro')
    plt.annotate("0,T", xy=ys[:,0],
                 xytext=ys[:,indicesPhasesToPlot[0]]+annotationGap, 
                 color="red", size=14)
    for i in xrange(1, len(indicesPhasesToPlot)):
        plt.annotate("%d/%dT"%(i, numberOfPhaseMarks), 
                     xy=ys[:,indicesPhasesToPlot[i]], 
                     xytext=ys[:,indicesPhasesToPlot[i]]+annotationGap, 
                     color="red", size=14)
    plt.grid()
    plt.legend(loc="upper left")
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.ylim((-0.1, 0.8))
    plt.savefig(aFigFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

