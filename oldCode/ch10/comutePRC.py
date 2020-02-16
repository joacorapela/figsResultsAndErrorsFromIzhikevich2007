
import sys
import pdb
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateModelForward

def computePRC(model, nSamples, i0, 
                      waitLC, waitLCPulse, 
                      pulseStrength=5.0, pulseWidthFactor=100, 
                      v0=-60.00, n0=0.0008, t0=0.0, 
                      dt = 1e-3):
    tf = (waitLC+waitLCPulse)*2.0
    nTSteps = int(round((tf-t0)/dt))
    times = np.empty(nTSteps+1)
    pulseWidth = pulseWidthFactor*dt
    def iDC(t):
        return(i0)
    iNapIKModelDC = INapIKModel.getHighThresholdInstance(i=iDC)
    y0 = np.array([v0, n0])
    resDC = integrateModelForward(model=iNapIKModelDC, 
                                   y0=y0, dt=dt, nTSteps=nTSteps)
    # start debug
    sampleWaitLC=np.argmin(np.abs(resDC["times"]-waitLC)
    plt.figure()
    plotHighThresholdINapIKVectorField(i=i0)
    plt.plot(ys[0, :], ys[1, :])
    plt.plot(ys[0, sampleWaitLC], ys[1, sampleWaitLC], mark="o", color="red")
    # end debug

    dcSpikeIndices = getPeakIndices(v=resDC["ys"][0,:])
    dcSpikeTimes = resDC["times"][dcSpikeIndices]
    dcSpikeIndicesAfterWait = np.nonzero(dcSpikeTimes>waitLC)[0]
    dcSpikeTimesAfterWait = dcSpikeTimes[dcSpikeIndicesAfterWait]
    ts = np.mean(dcSpikeTimesAfterWait[1:]-dcSpikeTimesAfterWait[:-1])
    T = mean(ts)

    # start debug
    show("mean(T)=%.2f, sd(T)=%.2f"%(T, sd(ts)))
    # end debug

    pulseTimes = dcSpikeTimesAfterWait[0]+np.arange(0, nSamples)*T/nSamples
    prc = np.empty(nSamples)
    for i in range(nSamples):
        pulseTime = pulseTimes[i]
        def iDCPulse(t):
            if pulseTime-pulseWidth/2<t and t<=pulseTime+pulseWidth/2:
                return(i0+pulseStrength)
            return(i0)
        iNapIKModelDCPulse = INapIKModel.getHighThresholdInstance(i=iDCPulse)
        resDCPulse = integrateModelForward(model=iNapIKModelDCPulse, 
                                            y0=y0, dt=dt, nTSteps=nTSteps)
        dcPulseSpikeIndices = getPeakIndices(v=resDCPulse["ys"][0,:])
        dcPulseSpikeTimes = resDCPulse["times"][dcPulseSpikeIndices]
        dcPulseSpikeIndicesAfterWait = np.nonzero(dcPulseSpikeTimes>(waitLC+waitLCPulse))[0]
        dcPulseSpikeTimesAfterWait = dcPulseSpikeTimes[dcPulseSpikeIndicesAfterWait]
        prc[i] = dcPulseSpikeTimesAfterWait[0]-dcSpikeTimesAfterWait[0]

    # start debug
    plt.plot(np.arange(0, nSamples)*T/nSamples, prc)
    plt.xlab("Time (ms)")
    plt.ylab("Time (ms)")
    # end debug
    return(prc)
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

