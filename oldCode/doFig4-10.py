

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField

def main(argv):
    phaseFigFilename = 'figures/fig4-10PhaseSpace.eps'
    voltageFigFilename = 'figures/fig4-10Voltage.eps'
    resultsFilenamePattern = 'results/integrationINapIKStepsize%d.npz'
    i0 = 40.0

    plt.figure()
    plotLowThresholdINapIKVectorField() 
    '''
    plotINapIKVectorField(I=i0, C=1.0, EL=-78, gL=8, gNa=20, gK=10, 
                                 VoneHalf_m=-20, k_m=15, 
                                 VoneHalf_n=-45, k_n=5, tauV=1, ENa=60,
                                 EK=-90, nDotScaleFactor=200, 
                                 vMin=-90.0, vMax=20.0, nVs=19, nVsDense=100,
                                 nMin=0.0, nMax=0.7, nNs=18, 
                                 vNullclineLabel="v nullcline",
                                 nNullclineLabel="n nullcline")
    '''
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')

    resultsFilename = resultsFilenamePattern % i0
    results = np.load(resultsFilename)
    plt.plot(results['ys'][0, :], results['ys'][1, :], label="%d"%i0)
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.savefig(phaseFigFilename)

    plt.figure()
    plt.plot(results['times'], results['ys'][0, :], label="%d"%i0)
    plt.grid()
    plt.legend()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

