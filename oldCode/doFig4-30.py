

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotINapIKVectorField

def main(argv):
    i0 = 10.0
    c = 1.0
    eL = -80
    gL = 8
    gNa = 20
    gK = 10
    mVOneHalf = -20
    mK = 15
    nVOneHalf = -25
    nK = 5
    tauV = 1.0
    eNa = 60
    eK = -90
    nMin = -0.1
    nMax = 0.7

    iPulseStrength = 0.0
    resultsFilenamePattern = 'results/integrationINapIKFig4-30PulseStrength%d.npz'
    phaseFigFilename = 'figures/fig4-30PhaseSpace.eps'
    voltageFigFilename = 'figures/fig4-30Voltage.eps'

    plt.figure()
    plotINapIKVectorField(I=i0, c=c, eL=eL, gL=gL, gNa=gNa, gK=gK, 
                                 mVOneHalf=mVOneHalf, mK=mK, 
                                 nVOneHalf=nVOneHalf, nK=nK, tauV=tauV, eNa=eNa,
                                 eK=eK, nDotScaleFactor=200, 
                                 vMin=-90.0, vMax=20.0, nVs=19, nVsDense=100,
                                 nMin=nMin, nMax=nMax, nNs=18, 
                                 vNullclineLabel="v nullcline",
                                 nNullclineLabel="n nullcline")
    resultsFilename = resultsFilenamePattern % iPulseStrength
    results = np.load(resultsFilename)
    ys = results["ys"]
    plt.plot(ys[0, :], ys[1, :], label="p=%d"%iPulseStrength)
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.savefig(phaseFigFilename)

    times = results["times"]
    plt.figure()
    plt.plot(times, ys[0, :], label="p=%d"%iPulseStrength)
    results.close()
    plt.grid()
    plt.legend()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

