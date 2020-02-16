
import sys
import pdb
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateModelForward, getPeakIndices

def main(argv):
    resultsFilename = 'results/integrationINapIKFig10_4LeftPanel_INapIKLowThreshold.npz'
    v0 = -60.00
    t0 = 0.0
    tf = 90.0
    dt = 1e-3
    nTSteps = int(round((tf-t0)/dt))
    times = np.empty(nTSteps+1)
    i0 = 35
    nTransientSpikes = 6
    pulsePhase = 45.0/50
    pulseStrength = 10.0
    pulseWidth = 100*dt

    def iDC(t):
        return(i0)
    iNapIKModelDC = INapIKModel.getLowThresholdInstance()
    iNapIKModelDC.setI(i=iDC)
    n0DC = iNapIKModelDC._nInf(v=v0)
    y0DC = np.array([v0, n0DC])
    resDC = integrateModelForward(model=iNapIKModelDC, 
                                   y0=y0DC, dt=dt, nTSteps=nTSteps)
    spikeIndices = getPeakIndices(v=resDC["ys"][0,:])
    if len(spikeIndices)<=nTransientSpikes:
        raise ValueError("nTransientSpikes=%d is too large"%(nTransientSpikes))
    spikeTimes = resDC["times"][spikeIndices]
    tPulse = spikeTimes[nTransientSpikes+1]+pulsePhase
    def iDCPulse(t):
        if tPulse-pulseWidth/2<t and t<=tPulse+pulseWidth/2:
            return(i0+pulseStrength)
        return(i0)
    iNapIKModelDCPulse = INapIKModel.getLowThresholdInstance()
    iNapIKModelDCPulse.setI(i=iDCPulse)
    n0DCPulse = iNapIKModelDCPulse._nInf(v=v0)
    y0DCPulse = np.array([v0, n0DCPulse])
    resDCPulse = integrateModelForward(model=iNapIKModelDCPulse, 
                                        y0=y0DCPulse, dt=dt, nTSteps=nTSteps)
    np.savez(resultsFilename, timesDC=resDC['times'], 
                              ysDC=resDC['ys'],
                              timesDCPulse=resDCPulse['times'],
                              ysDCPulse=resDCPulse['ys'],)

    plt.plot(resDC["times"], resDC["ys"][0,:], label="DC")
    plt.plot(resDCPulse["times"], resDCPulse["ys"][0,:], label="Pulse")
    plt.axvline(x=spikeTimes[nTransientSpikes+1]+pulsePhase, color="red")
    plt.legend(loc="lower right")
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane Potential (mV)")
    plt.xlim((tPulse-10, tPulse+20))
    plt.title("Pulse Phase %.02f"%(pulsePhase))
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

