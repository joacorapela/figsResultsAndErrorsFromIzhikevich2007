
import sys
import pdb
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateForward, getPeakIndices

def main(argv):
    resultsFilename = "results/integrationINapIKFig10_10_matching1-1Sync.npz"
    v0 = -60.00
    t0 = 0.0
    tf = 400.0
    dt = 1e-3
    nTSteps = int(round((tf-t0)/dt))
    times = np.empty(nTSteps+1)
    i0 = 10.0
    nTransientSpikes = 6
    pulsePhase = 2.5
    pulseStrength = 20.0
    pulseWidthFactor = 100
    Ts = 6.795

    pulseWidth = pulseWidthFactor*dt
    def iDC(t):
        return(i0)
    iNapIKModelDC = INapIKModel.getHighThresholdInstance()
    iNapIKModelDC.setI(i=iDC)
    n0DC = iNapIKModelDC._nInf(v=v0)
    y0DC = np.array([v0, n0DC])
    resDC = integrateForward(deriv=iNapIKModelDC.deriv, t0=t0, y0=y0DC, dt=dt,
                                                        nTSteps=nTSteps)
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
    model = INapIKModel.getHighThresholdInstance()
    model.setI(i=iDCTrainPulses)
    n0 = model._nInf(v=v0)
    y0 = np.array([v0, n0])
    resDCTrainPulses = integrateForward(deriv=model.deriv, t0=t0, y0=y0, dt=dt, 
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

    ts = spikeTimes[1:]-spikeTimes[:-1]
    T = np.mean(ts)
    print("T=%.02f"%(T))
    pdb.set_trace()

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

