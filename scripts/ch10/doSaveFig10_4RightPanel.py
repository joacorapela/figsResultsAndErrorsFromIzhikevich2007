
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import computePRC

def main(argv):
    resultsFilename = 'results/prcINapIKFig10_4RightPanel.npz'
    figFilename = 'figures/fig10_4RightPanel.eps'
    v0 = -60.00
    t0 = 0.0
    tf = 90.0
    dt = 1e-3
    i0 = 4.7
    pulseStrength = 10.0
    pulseWidthFactor = 100
    nSamples = 30
    waitLC = 100.0
    waitLCPulse = 100.0

    model = INapIKModel.getHighThresholdInstance()
    n0 = model._nInf(v=v0)
    prcRes = computePRC(model=model, nSamples=nSamples, i0=i0, 
                         waitLC=waitLC, waitLCPulse=waitLCPulse, 
                         pulseStrength=pulseStrength, pulseWidthFactor=pulseWidthFactor, 
                         v0=v0, n0=n0, t0=t0, dt=dt)
    np.savez(resultsFilename, prc=prcRes['prc'], phases=prcRes['phases'],
                              T=prcRes["T"])
    plt.plot(prcRes['phases'], prcRes['prc'], marker="o")
    plt.xlabel("Phase (ms)")
    plt.ylabel("Phase Reset (ms)")
    plt.savefig(figFilename)
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

