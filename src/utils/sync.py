
import sys
import pdb
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
sys.path.append("../../src")
from signalProcessing.utils import lowpassKaiser
from utils.misc import getPeakIndices

def malkinsHFunc(qsi, qsiTimes, xsi, xsiTimes, xsj, xsjTimes, coupling, phaseDiff, T):
    def integrand(t):
        qsiTIndex = np.argmin(np.abs(t-qsiTimes))
        xsiTIndex = np.argmin(np.abs(t-xsiTimes))
        xsjTPlusPhaseDiffIndex = np.argmin(np.abs(t+phaseDiff-xsjTimes))
        couplingVector = coupling(xsi[:, xsiTIndex], 
                                   xsj[:, xsjTPlusPhaseDiffIndex])
        answer = qsi[:,qsiTIndex].dot(couplingVector)
        return answer
    answer = 1.0/T*integrate.quad(integrand, 0, T)[0]

    # begin debug
    # qsi0 = qsi[0]
    # dtXsj = np.mean(xsjTimes[1:]-xsjTimes[:-1])
    # phaseDiffInSamples = phaseDiff/dtXsj
    # xsjShifted = xsj[:,phaseDiffInSamples:]
    # xsjShiftedTrimmed = xsjShifted[0,:len(qsiTimes)] 
    # xiTrimmed = xsi[0,:len(qsiTimes)]
    # xsjShiftedTrimmedMinusXiTrimmed =  xsjShiftedTrimmed - xiTrimmed 
    # dtQis = np.mean(qsiTimes[1:]-qsiTimes[:-1])
    # answer2 = 1.0/T*np.sum(qsi0*xsjShiftedTrimmedMinusXiTrimmed)*dtQis

    # def integrand2(t):
        # qsiTIndex = np.argmin(np.abs(t-qsiTimes))
        # xsiTIndex = np.argmin(np.abs(t-xsiTimes))
        # answer = qsi[0,qsiTIndex]*(xsjShifted[0,xsiTIndex]-xsi[0,xsiTIndex])
        # return answer
    # answer3 = 1.0/T*integrate.quad(integrand2, 0, T)[0]

    # print("answer=%f, answer2=%f , answer3=%f" %(answer, answer2, answer3))
    # ax = plt.gca()
    # ax.plot(qsiTimes, xsjShiftedTrimmed, label="xj")
    # ax.plot(qsiTimes, xiTrimmed, label="xi")
    # ax.plot(qsiTimes, xsjShiftedTrimmedMinusXiTrimmed, label="xj-xi")
    # ax.axhline(y=0, color="gray")
    # ax2 = ax.twinx()
    # ax2.plot(qsiTimes, qsi0, '--', label="qsi0")
    # ax.legend(loc="upper left")
    # ax2.legend(loc="upper right")
    # ax2.axhline(y=0, color="gray", linestyle="--")
    # plt.show()
    # end debug

    return answer

def getPhasesFromVoltages(times, voltages,
                                 cutoffHz=4, transitionWidthHz=1.0, 
                                 rippleDB=60, doPlots=False):
    sampleRate = 1.0/np.mean(times[1:]-times[:-1])
    res = lowpassKaiser(t=times, x=voltages, cutoffHz=cutoffHz, 
                                 transitionWidthHz=transitionWidthHz,
                                 rippleDB=rippleDB,
                                 sampleRate=sampleRate,
                                 doPlots=doPlots)
    lpTimes = res["t"]
    lpVoltages = res["x"]
    spikeSamples = getPeakIndices(v=lpVoltages)
    ts = (np.array(spikeSamples[1:])-np.array(spikeSamples[:-1]))/sampleRate
    lpVoltagesInRange = lpVoltages[spikeSamples[0]:spikeSamples[-1]]
    lpTimesInRange = lpTimes[spikeSamples[0]:spikeSamples[-1]]
    spikeSamplesInRange = spikeSamples-spikeSamples[0]
    lpVoltagesInRangeIndices = range(len(lpVoltagesInRange))
    phases = np.empty(len(lpVoltagesInRangeIndices))
    lastSpikeSample = spikeSamplesInRange[0]
    for i in np.arange(1, len(spikeSamplesInRange)):
        nextSpikeSample = spikeSamplesInRange[i]
        indicesBtwLastAndNextSpikeSample = np.nonzero(np.logical_and(lastSpikeSample<=lpVoltagesInRangeIndices, lpVoltagesInRangeIndices<nextSpikeSample))[0]
        # phases[indicesBtwLastAndNextSpikeSample] = (indicesBtwLastAndNextSpikeSample-lastSpikeSample)/float(len(indicesBtwLastAndNextSpikeSample))
        phases[indicesBtwLastAndNextSpikeSample] = (indicesBtwLastAndNextSpikeSample-lastSpikeSample)/sampleRate
        lastSpikeSample = nextSpikeSample
    return {"times": lpTimesInRange, "phases":phases,
            "spikeTimes":spikeSamples/sampleRate}
