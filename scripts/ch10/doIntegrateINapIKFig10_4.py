
import sys
import pdb
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateModelForward

def main(argv):
    resultsFilename = 'results/integrationINapIKFig10_4LeftPanel.npz'
    v0 = -60.00
    n0 = 0.0008
    t0 = 0.0
    tf = 90.0
    dt = 1e-3
    nTSteps = int(round((tf-t0)/dt))
    times = np.empty(nTSteps+1)
    i0 = 4.7
    tPulse = 18
    pulseStrength = 7.0
    pulseWidth = 100*dt
    def iDC(t):
        return(i0)
    def iDCPulse(t):
        if tPulse-pulseWidth/2<t and t<=tPulse+pulseWidth/2:
            return(i0+pulseStrength)
        return(i0)
    iNapIKModelDC = INapIKModel.getHighThresholdInstance()
    iNapIKModelDC.setI(i=iDC)
    n0DC = iNapIKModelDC._nInf(v=v0)
    y0DC = np.array([v0, n0DC])
    iNapIKModelDCPulse = INapIKModel.getHighThresholdInstance()
    iNapIKModelDCPulse.setI(i=iDCPulse)
    n0DCPulse = iNapIKModelDCPulse._nInf(v=v0)
    y0DCPulse = np.array([v0, n0DCPulse])
    resDC = integrateModelForward(model=iNapIKModelDC, 
                                   y0=y0DC, dt=dt, nTSteps=nTSteps)
    resDCPulse = integrateModelForward(model=iNapIKModelDCPulse, 
                                        y0=y0DCPulse, dt=dt, nTSteps=nTSteps)
    np.savez(resultsFilename, timesDC=resDC['times'], 
                              ysDC=resDC['ys'],
                              timesDCPulse=resDCPulse['times'],
                              ysDCPulse=resDCPulse['ys'],)

    plt.plot(resDC["times"], resDC["ys"][0,:], label="DC")
    plt.plot(resDCPulse["times"], resDCPulse["ys"][0,:], label="Pulse")
    # plt.axvline(x=tPulse, color="red")
    plt.legend(loc="lower right")
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane Potential (mV)")
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

