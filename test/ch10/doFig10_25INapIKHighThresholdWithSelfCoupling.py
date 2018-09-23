
import sys
import numpy as np
import pickle
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

    if len(argv)!=2:
        print("Usage: %s <selfCouplingStrength>"%argv[0])
        sys.exit(1)

    selfCouplingStrength = float(argv[1])
    epsilon = 0.1
    i0 = 10
    couplingStartTime = 99.04
    colorNeuron0 = "blue"
    colorNeuron1 = "green"
    linestyleCoupled = "-"
    linestyleUncoupled = ":"
    integrationFilename = "results/integrationWCoupledINapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime)
    figFilenamePattern = "figures/fig10_25INapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.%s"

    figFilename = figFilenamePattern%(selfCouplingStrength, i0, epsilon, 
                                                            couplingStartTime, 
                                                            "eps")
    res = np.load(integrationFilename)
    timesCoupled = res["timesCoupled"]
    voltagesCoupledNeuron0 = res["ysCoupled"][0,:]
    voltagesCoupledNeuron1 = res["ysCoupled"][2,:]
    voltagesUncoupledNeuron0 = res["ys0Uncoupled"][0,:]
    timesUncoupledNeuron0 = res["times0Uncoupled"]
    voltagesUncoupledNeuron1 = res["ys1Uncoupled"][0,:]
    timesUncoupledNeuron1 = res["times1Uncoupled"]
    sampleRate = 1.0/(timesCoupled[1]-timesCoupled[0])

    resPhasesNeuron0 = getPhasesFromVoltages(times=timesCoupled, 
                                              voltages=voltagesCoupledNeuron0)
    phasesNeuron0 = resPhasesNeuron0["phases"]
    timePhasesNeuron0 = resPhasesNeuron0["times"]
    resPhasesNeuron1 = getPhasesFromVoltages(times=timesCoupled,
                                              voltages=voltagesCoupledNeuron1)
    phasesNeuron1 = resPhasesNeuron1["phases"]
    timePhasesNeuron1 = resPhasesNeuron1["times"]
    spikeTimesNeuron0 = resPhasesNeuron0["spikeTimes"]
    uncoupledSpikeTimesNeuron0 = spikeTimesNeuron0[spikeTimesNeuron0<couplingStartTime]
    ts = uncoupledSpikeTimesNeuron0[1:]-uncoupledSpikeTimesNeuron0[:-1]
    T = np.mean(ts)
    phasesUncoupledNeuron0 = (range(len(voltagesCoupledNeuron0))/sampleRate)%T
    timePhasesUncoupledNeuron0 = range(len(voltagesCoupledNeuron0))/sampleRate

    align0Res = alignMeasurements(times0=timePhasesNeuron0,
                                   measurements0=phasesNeuron0,
                                   times1=timePhasesUncoupledNeuron0,
                                   measurements1=phasesUncoupledNeuron0)
    # phaseDeviationsNeuron0 = computeCircularVariances(phases1=align0Res["alignedMeasurements0"]*2*np.pi/T, phases2=align0Res["alignedMeasurements1"]*2*np.pi/T)*T/2.0
    phaseDeviationsNeuron0 = (align0Res["alignedMeasurements0"]-align0Res["alignedMeasurements1"])%T
    # begin debug
    # plt.plot(align0Res["alignedTimes0"], align0Res["alignedMeasurements0"], label=r"coupled $\theta_0$")
    # plt.plot(align0Res["alignedTimes1"], align0Res["alignedMeasurements1"], label=r"uncoupled $\theta_1$")
    # plt.plot(align0Res["alignedTimes0"], phaseDeviationsNeuron0, label=r"$\varphi_0$")
    # plt.axvline(x=couplingStartTime, color="red")
    # plt.legend()
    # plt.show()
    # pdb.set_trace()
    # end debug
    align1Res = alignMeasurements(times0=timePhasesNeuron1,
                                   measurements0=phasesNeuron1,
                                   times1=timePhasesUncoupledNeuron0,
                                   measurements1=phasesUncoupledNeuron0)
    # phaseDeviationsNeuron1 = computeCircularVariances(phases1=align1Res["alignedMeasurements0"]*2*np.pi/T, phases2=align1Res["alignedMeasurements1"]*2*np.pi/T)*T/2.0
    phaseDeviationsNeuron1 = (align1Res["alignedMeasurements0"]-align1Res["alignedMeasurements1"])%T

    align3Res = alignMeasurements(times0=align0Res["alignedTimes0"],
                                   measurements0=phaseDeviationsNeuron0,
                                   times1=align1Res["alignedTimes0"],
                                   measurements1=phaseDeviationsNeuron1)
    phaseDifs = align3Res["alignedMeasurements0"]-align3Res["alignedMeasurements1"]

    ax1 = plt.subplot(411)
    plt.plot(timesCoupled, voltagesCoupledNeuron0, color=colorNeuron0,
                    linestyle=linestyleCoupled, label=r"coupled $V_0$")
    plt.plot(timesCoupled, voltagesCoupledNeuron1, color=colorNeuron1,
                    linestyle=linestyleCoupled, label=r"coupled $V_1$")
    plt.plot(timesUncoupledNeuron0, voltagesUncoupledNeuron0, 
                                    color=colorNeuron0,
                                    linestyle=linestyleUncoupled, 
                                    label=r"uncoupled $V_0$")
    plt.plot(timesUncoupledNeuron1, voltagesUncoupledNeuron1, 
                                    color=colorNeuron1,
                                    linestyle=linestyleUncoupled, 
                                    label=r"uncoupled $V_1$")
    plt.grid()
    plt.ylabel("Membrane\nPotential (mV)")
    plt.legend()
    plt.axvline(x=couplingStartTime, color="red")
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2= plt.subplot(412, sharex=ax1)
    plt.plot(resPhasesNeuron0["times"], resPhasesNeuron0["phases"],
                                        color=colorNeuron0,
                                        linestyle=linestyleCoupled,
                                        label=r"coupled $\theta_0$")
    plt.plot(resPhasesNeuron1["times"], resPhasesNeuron1["phases"],
                                        color=colorNeuron1,
                                        linestyle=linestyleCoupled,
                                        label=r"coupled $\theta_1$")
    plt.plot(timePhasesUncoupledNeuron0, phasesUncoupledNeuron0,
                                          color=colorNeuron0,
                                          linestyle=linestyleUncoupled,
                                          label=r"uncoupled $\theta_0$")
    plt.grid()
    plt.ylabel("Phase (sec)")
    plt.legend()
    plt.axvline(x=couplingStartTime, color="red")
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax3= plt.subplot(413, sharex=ax1)
    plt.plot(align0Res["alignedTimes0"], phaseDeviationsNeuron0,
                                         label=r"$\varphi_0$")
    plt.plot(align1Res["alignedTimes0"], phaseDeviationsNeuron1,
                                         label=r"$\varphi_1$")
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

