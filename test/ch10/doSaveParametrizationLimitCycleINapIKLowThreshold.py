
import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel
from WeaklyCoupledOscillatorsModel import WeaklyCoupledOscillatorsModel
from utils import integrateForward, getPeakIndices

def main(argv):
    i0 = 35.0
    v0 = -26.21
    n0 = 0.45
    dt = 1e-3
    burnTime = 1.0 # seconds
    t0 = 0.0
    tf = 10.0
    nTSteps = int((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    resultsFilename = "results/paramLimitCyclesINapIKLowThresholdI0%.02f.npz"%(i0)
    voltagesFigFilename = "figures/voltagesParamLimitCycleInapIKLowThresholdI0%.02f.eps"%(i0)
    phaseSpaceFigFilename = "figures/phaseSpaceParamLimitCycleInapIKLowThresholdI0%.02f.eps"%(i0)

    def i(t):
        return(i0)
    iNapIKModel = INapIKModel.getLowThresholdInstance()
    iNapIKModel.setI(i=i)

    y0 = np.array([v0, n0])
    res = integrateForward(deriv=iNapIKModel.deriv, t0=t0, y0=y0, dt=dt,
                                                    nTSteps=nTSteps)
    ys = res["ys"]
    times= res["times"]

    burnTimeIndex = np.nonzero(times>burnTime)[0][0]
    ysAfterBurnTime =ys[:,burnTimeIndex:]
    timesAfterBurnTime = times[burnTimeIndex:]
    peakIndices = getPeakIndices(v=ysAfterBurnTime[0,:])
    limitCycle = ysAfterBurnTime[:, peakIndices[0]:peakIndices[1]]
    phases = np.arange(peakIndices[0], peakIndices[1])*dt
    phases = phases-phases[0]

    np.savez(resultsFilename, phases=phases,  limitCycle=limitCycle)

    plt.plot(phases, limitCycle[0,:])
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane potential (mV)")
    plt.savefig(voltagesFigFilename)

    plt.figure()
    plt.plot(limitCycle[0,:], limitCycle[1,:])
    plt.grid()
    plt.xlabel("Membrane potential (mV)")
    plt.ylabel("Activation gate, n")
    plt.savefig(phaseSpaceFigFilename)

    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

