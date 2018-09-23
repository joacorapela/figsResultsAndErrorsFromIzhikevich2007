
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import getPhasesFromVoltages
from circularStats import circularVariance
from utils import alignMeasurements

def main(argv):
    def computeCircularVariances(phases1, phases2):
        cvs = np.empty(len(phases1))
        for i in xrange(len(phases1)):
            cvs[i] = circularVariance(angles=(phases1[i], phases2[i]))
        return cvs

    epsilon = 5.0*1e-4
    i0 = 10
    couplingStartTime = 100.0
    integrationFilename = "results/integrationWCoupledINapIKI0%.02fEpsilon%.02fCouplingStart%.02f.npz"%(i0, epsilon, couplingStartTime)
    figFilename = "figures/phaseDeviationsWCoupledINapIKI0%.02fEpsilon%.02fCouplingStart%.02f.eps"%(i0, epsilon, couplingStartTime)

    res = np.load(integrationFilename)
    times = res["times"]
    voltagesNeuron1 = res["ys"][0,:]
    voltagesNeuron2 = res["ys"][2,:]
    sampleRate = 1.0/(times[1]-times[0])

    resNeuron1 = getPhasesFromVoltages(times=times, voltages=voltagesNeuron1)
    phasesNeuron1 = resNeuron1["phases"]*2*np.pi
    timePhasesNeuron1 = resNeuron1["times"]
    resNeuron2 = getPhasesFromVoltages(times=times, voltages=voltagesNeuron2)
    phasesNeuron2 = resNeuron2["phases"]*2*np.pi
    timePhasesNeuron2 = resNeuron2["times"]
    spikeTimesNeuron1 = resNeuron1["spikeTimes"]
    uncoupledSpikeTimesNeuron1 = spikeTimes[spikeTimesNeuron1<couplingStartTime]
    ts = uncoupledSpikeTimesNeuron1[1:]-uncoupledSpikeTimesNeuron1[:-1]
    T = np.mean(ts)
    analyticalPhasesUncoupledNeuron1 = ((range(len(voltagesNeuron1))/sampleRate)%T)/T*2*np.pi
    timeAnalyticalPhasesUncoupledNeuron1 = range(len(voltagesNeuron1))/sampleRate

    align1Res = alignMeasurements(times1=timePhasesNeuron1,
                                   measurements1=phasesNeuron1,
                                   times2=timeAnalyticalPhasesUncoupledNeuron1,
                                   measurements2=analyticalPhasesUncoupledNeuron1)
    phaseDeviationsNeuron1 = computeCircularVariances(phases1=align1Res["alignedMeasurements1"],
                                                       phases2=align1Res["alignedMeasurements2"])
    align2Res = alignMeasurements(times1=timePhasesNeuron2,
                                   measurements1=phasesNeuron2,
                                   times2=timeAnalyticalPhasesUncoupledNeuron1,
                                   measurements2=analyticalPhasesUncoupledNeuron1)
    phaseDeviationsNeuron2 = computeCircularVariances(phases1=align2Res["alignedMeasurements1"],
                                                       phases2=align2Res["alignedMeasurements2"])
    plt.plot(align1Res["alignedTimes1"], phaseDeviationsNeuron1, label=r"$\varphi1$")
    plt.plot(align2Res["alignedTimes1"], phaseDeviationsNeuron2, label=r"$\varphi2$")
    plt.legend()
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Phase Deviation")
    plt.savefig(figFilename)

    align3Res = alignMeasurements(times1=align1Res["alignedTimes1"],
                                   measurements1=phaseDeviationsNeuron1,
                                   times2=align2Res["alignedTimes1"],
                                   measurements2=phaseDeviationsNeuron2)
    phaseDifs = align3Res["alignedMeasurements1"]-align3Res["alignedMeasurements2"]

    plt.figure()
    plt.plot(align3Res["alignedTimes1"], phaseDifs)
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Phase Difference")

    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

