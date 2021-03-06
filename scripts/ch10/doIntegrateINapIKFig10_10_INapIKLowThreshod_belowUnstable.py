
import sys
import pdb
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateModelForward, getPeakIndices

def main(argv):
    resultsFilename = "results/integrationINapIKFig10_10_INapIKLowThreshold_belowUnstable.npz"
    v0 = -60.00
    t0 = 0.0
    tf = 800.0
    dt = 1e-3
    nTSteps = int(round((tf-t0)/dt))
    times = np.empty(nTSteps+1)
    i0 = 50
    nTransientSpikes = 6
    pulsePhase = 0.44
    pulseStrength = 10.0
    pulseWidthFactor = 100
    Ts = 3.403

    pulseWidth = pulseWidthFactor*dt
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
    def iDCTrainPulses(t):
        if t>tPulse:
            r = (t-tPulse)%Ts
            if r<pulseWidth/2 or Ts-pulseWidth/2<r:
                return(i0+pulseStrength)
        return(i0)
    model = INapIKModel.getLowThresholdInstance()
    model.setI(i=iDCTrainPulses)
    n0 = model._nInf(v=v0)
    y0 = np.array([v0, n0])
    resDCTrainPulses = integrateModelForward(model=model, y0=y0, dt=dt, 
                                                          nTSteps=nTSteps)
    # peakIndices = getPeakIndices(v=resDCTrainPulses["ys"][0,:])
    # resDCTrainPulses["ys"] = resDCTrainPulses["ys"][:,peakIndices[0]:]
    # resDCTrainPulses["times"] = resDCTrainPulses["times"][peakIndices[0]:]-\
    #                             resDCTrainPulses["times"][peakIndices[0]]

    appliedIs = np.empty(resDCTrainPulses["times"].shape)
    for i in range(len(resDCTrainPulses["times"])):
        appliedIs[i] = iDCTrainPulses(t=resDCTrainPulses["times"][i])

    np.savez(resultsFilename, 
              timesDC=resDC["times"],
              ysDC=resDC["ys"],
              timesDCTrainPulses=resDCTrainPulses["times"],
              ysDCTrainPulses=resDCTrainPulses["ys"],
              i0=i0, i=appliedIs, Ts=Ts, tPulse=tPulse)

    plt.plot(resDC["times"], resDC["ys"][0,:], color="blue", label="DC stim")
    plt.plot(resDCTrainPulses["times"], resDCTrainPulses["ys"][0,:], color="magenta", label="Pulse stim")
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane Potential (mV)")
    plt.legend(loc="upper left")
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(resDCTrainPulses["times"], appliedIs, color="lightgray")
    ax2.set_ylabel("Input Current (mA)")
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

