
import sys
import pdb
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateModelForward, getPeakIndices

def main(argv):
    resultsFilename = "results/integrationINapIKFig10_10.npz"
    v0 = -60.00
    t0 = 0.0
    tf = 198.0
    dt = 1e-3
    nTSteps = int(round((tf-t0)/dt))
    times = np.empty(nTSteps+1)
    i0 = 4.7
    pulseStrength = 10.0
    pulseWidth = 100*dt
    Ts = 18.37
    offset = 9.0
    # offset = 14.0
    def iDCTrainPulses(t):
        r = (t-offset)%Ts
        if r<pulseWidth/2 or Ts-pulseWidth/2<r:
            return(i0+pulseStrength)
        return(i0)
    model = INapIKModel.getHighThresholdInstance()
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

    np.savez(resultsFilename, times=resDCTrainPulses["times"],
                              ys=resDCTrainPulses["ys"],
                              i0=i0, i=appliedIs, Ts=Ts, offset=offset)

    plt.plot(resDCTrainPulses["times"], resDCTrainPulses["ys"][0,:], color="blue")
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane Potential (mV)")
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(resDCTrainPulses["times"], appliedIs, color="lightgray")
    ax2.set_ylabel("Input Current (mA)")
    plt.show()

if __name__ == "__main__":
    main(sys.argv)

