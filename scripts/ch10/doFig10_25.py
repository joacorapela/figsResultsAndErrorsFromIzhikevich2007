
import sys
import numpy as np
import pickle
import pdb
import matplotlib.pyplot as plt
sys.path.append("../../src")
from utils.sync import getPhasesFromVoltages
from utils.misc import alignMeasurements
from stats.circular import circularVariance

def main(argv):
    def computeCircularVariances(phases1, phases2):
        cvs = np.empty(len(phases1))
        for i in xrange(len(phases1)):
            cvs[i] = circularVariance(angles=(phases1[i], phases2[i]))
        return cvs

    epsilon = 2.5*1e-4
    i0 = 10
    couplingStartTime = 100.0
    integrationFilename = "results/integrationWCoupledINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    figFilenamePattern = "figures/fig10_25I0%.02fEpsilon%.06fCouplingStart%.02f.%s"

    figFilename = figFilenamePattern%(i0, epsilon, couplingStartTime, 
                                          "eps")
    figPickleFilename = figFilenamePattern%(i0, epsilon, couplingStartTime,
                                                "pickle")

    res = np.load(integrationFilename)
    times = res["times"]
    voltagesNeuron1 = res["ys"][0,:]
    voltagesNeuron2 = res["ys"][2,:]
    sampleRate = 1.0/(times[1]-times[0])

    resPhasesNeuron1 = getPhasesFromVoltages(times=times, 
                                              voltages=voltagesNeuron1)
    phasesNeuron1 = resPhasesNeuron1["phases"]*2*np.pi
    timePhasesNeuron1 = resPhasesNeuron1["times"]
    resPhasesNeuron2 = getPhasesFromVoltages(times=times,
                                              voltages=voltagesNeuron2)
    phasesNeuron2 = resPhasesNeuron2["phases"]*2*np.pi
    timePhasesNeuron2 = resPhasesNeuron2["times"]
    spikeTimesNeuron1 = resPhasesNeuron1["spikeTimes"]
    uncoupledSpikeTimesNeuron1 = spikeTimesNeuron1[spikeTimesNeuron1<couplingStartTime]
    ts = uncoupledSpikeTimesNeuron1[1:]-uncoupledSpikeTimesNeuron1[:-1]
    T = np.mean(ts)
    phasesUncoupledNeuron1 = ((range(len(voltagesNeuron1))/sampleRate)%T)/T*2*np.pi
    timePhasesUncoupledNeuron1 = range(len(voltagesNeuron1))/sampleRate

    align1Res = alignMeasurements(times1=timePhasesNeuron1,
                                   measurements1=phasesNeuron1,
                                   times2=timePhasesUncoupledNeuron1,
                                   measurements2=phasesUncoupledNeuron1)
    phaseDeviationsNeuron1 = computeCircularVariances(phases1=align1Res["alignedMeasurements1"],
                                                       phases2=align1Res["alignedMeasurements2"])
    align2Res = alignMeasurements(times1=timePhasesNeuron2,
                                   measurements1=phasesNeuron2,
                                   times2=timePhasesUncoupledNeuron1,
                                   measurements2=phasesUncoupledNeuron1)
    phaseDeviationsNeuron2 = computeCircularVariances(phases1=align2Res["alignedMeasurements1"],
                                                       phases2=align2Res["alignedMeasurements2"])

    align3Res = alignMeasurements(times1=align1Res["alignedTimes1"],
                                   measurements1=phaseDeviationsNeuron1,
                                   times2=align2Res["alignedTimes1"],
                                   measurements2=phaseDeviationsNeuron2)
    phaseDifs = align3Res["alignedMeasurements1"]-align3Res["alignedMeasurements2"]

    ax1 = plt.subplot(411)
    plt.plot(times, voltagesNeuron1, label=r"$V_1$")
    plt.plot(times, voltagesNeuron2, label=r"$V_2$")
    plt.grid()
    plt.ylabel("Membrane\nPotential (mV)")
    plt.legend()
    plt.axvline(x=couplingStartTime, color="red")
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2= plt.subplot(412, sharex=ax1)
    plt.plot(resPhasesNeuron1["times"], resPhasesNeuron1["phases"], 
                                        label=r"$\theta_1$")
    plt.plot(resPhasesNeuron2["times"], resPhasesNeuron2["phases"],
                                        label=r"$\theta_2$")
    plt.grid()
    plt.ylabel("Phase (sec)")
    plt.legend()
    plt.axvline(x=couplingStartTime, color="red")
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax3= plt.subplot(413, sharex=ax1)
    plt.plot(align1Res["alignedTimes1"], phaseDeviationsNeuron1, label=r"$\varphi1$")
    plt.plot(align2Res["alignedTimes1"], phaseDeviationsNeuron2, label=r"$\varphi2$")
    plt.grid()
    plt.ylabel("Phase\nDeviation")
    plt.legend()
    plt.axvline(x=couplingStartTime, color="red")
    plt.setp(ax3.get_xticklabels(), visible=False)

    ax4= plt.subplot(414, sharex=ax1)
    plt.plot(align3Res["alignedTimes1"], phaseDifs)
    plt.grid()
    plt.ylabel("Phase\nDifference")
    plt.axvline(x=couplingStartTime, color="red")
    plt.xlabel("Time (sec)")

    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

