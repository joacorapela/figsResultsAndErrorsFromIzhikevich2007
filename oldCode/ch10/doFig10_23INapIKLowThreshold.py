
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):
    epsilon = 0.003
    i0 = 35.0
    couplingStartTime = 100.44
    # oscillatorIndex = 0
    oscillatorIndex = 1
    resultsFilename = "results/integrationQINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f_oscillator%d.npz"%(i0, epsilon, couplingStartTime, oscillatorIndex)
    figFilenamePattern = 'figures/fig10_23_INapIKLowhThreshold_%s.eps'
    # figFilenamePattern = "figures/integrationQINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f_oscillator%d_%s.eps"
    qIntRes = np.load(resultsFilename)

    plt.plot(qIntRes["times"], qIntRes["ys"][0,:], label="Q0", color="blue")
    plt.plot(qIntRes["times"], 0.01*qIntRes["ys"][1,:], label="0.01 Q1", color="red")
    # plt.ylim((-0.4, 0.3))
    plt.xlabel("Time (sec)")
    plt.ylabel("Q")
    plt.legend(loc="lower right")
    plt.savefig(figFilenamePattern%("QsVsTime"))

    plt.figure()
    plt.plot(qIntRes["ys"][0,:], qIntRes["ys"][1,:], color="blue")
    plt.xlabel("Q1")
    plt.ylabel("Q2")
    # plt.xlim((-0.1, 0.3))
    # plt.ylim((-50.0, 10.0))
    plt.savefig(figFilenamePattern%("Q1VsQ2"))

    plt.show()

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

