

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotINapIKVectorField

def main(argv):
    iPulseStrength = 1000000
    resultsFilenamePattern = 'results/integrationINapIKFig4-23PulseStrength%d.npz'
    phaseFigFilename = 'figures/fig4-23PhaseSpace.eps'
    voltageFigFilename = 'figures/fig4-23Voltage.eps'

    plt.figure()
    plotINapIKVectorField(I=3.0, c=1.0, eL=-80, gL=8, gNa=20, gK=10, 
                                 mVOneHalf=-20, mK=15, 
                                 nVOneHalf=-25, nK=5, tauV=0.152, eNa=60,
                                 eK=-90, nDotScaleFactor=200, 
                                 vMin=-90.0, vMax=20.0, nVs=19, nVsDense=100,
                                 nMin=0.0, nMax=0.7, nNs=18, 
                                 vNullclineLabel="v nullcline",
                                 nNullclineLabel="n nullcline")
    resultsFilename = resultsFilenamePattern % iPulseStrength
    results = np.load(resultsFilename)
    plt.plot(results['ys'][0, :], results['ys'][1, :],
                                  label="p=%d"%iPulseStrength)
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.savefig(phaseFigFilename)

    plt.figure()
    plt.plot(results['times'], results['ys'][0, :],
                               label="p=%d"%iPulseStrength)
    results.close()
    plt.grid()
    plt.legend()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

