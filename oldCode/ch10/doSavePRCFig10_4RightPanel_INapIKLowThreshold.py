
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import computePRC

def main(argv):
    resultsFilename = 'results/prcINapIKFig10_4RightPanel_INapIKLowThreshold.npz'
    figFilename = 'figures/fig10_4RightPanel_INapIKLowThreshold.eps'
    v0 = -60.00
    t0 = 0.0
    tf = 90.0
    dt = 1e-3
    i0 = 50
    pulseStrength = 10.0
    pulseWidthFactor = 100
    nSamples = 150
    waitLC = 100.0
    waitLCPulse = 100.0
    doPlots = False

    model = INapIKModel.getLowThresholdInstance()
    n0 = model._nInf(v=v0)
    prcRes = computePRC(model=model, nSamples=nSamples, i0=i0, 
                         waitLC=waitLC, waitLCPulse=waitLCPulse, 
                         pulseStrength=pulseStrength, pulseWidthFactor=pulseWidthFactor, 
                         v0=v0, n0=n0, t0=t0, dt=dt, doPlots=doPlots)
    np.savez(resultsFilename, prc=prcRes['prc'], phases=prcRes['phases'],
                              T=prcRes["T"])
    prc = prcRes['prc']
    phases = prcRes['phases']
    dPhase = phases[1]-phases[0]
    dPRC = np.empty(len(prc))
    dPRC[1:] = (prc[1:]-prc[:-1])/dPhase
    dPRC[0] = (prc[0]-prc[-1])/dPhase

    plt.plot(phases, prc, marker="o", color="blue")
    plt.xlabel("Phase (ms)")
    plt.ylabel("Phase Reset (ms)")
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(phases, dPRC, color="magenta")
    plt.savefig(figFilename)
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

