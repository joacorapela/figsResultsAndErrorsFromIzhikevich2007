
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):

    iNapIKResultsFilenamePattern = "results/integrationINapIKIExampleP163_i0%.02fv0%.02f.npz"
    normalFormResultsFilenamePattern = "results/analyticalSolutionNormalFormExampleP163_i0%.02fv0%.02f.npz"
    figFilename = "figures/dynamicsINapIKAndNormalFormExampleP163.eps"
    i0s = (-5.0,)
#     v0s = (-45.0, -57.0, -75.0)
    v0s = (-45.0, -41.0, -11.0)
    for i0 in i0s:
        for v0 in v0s:
            iNapIKResultsFilename = iNapIKResultsFilenamePattern%(i0,v0)
            normalFormResultsFilename = normalFormResultsFilenamePattern%(i0,v0)
            iNapIKResults = np.load(iNapIKResultsFilename)
            iNapIKYs = iNapIKResults["ys"]
            iNapIKTimes = iNapIKResults["times"]
            normalFormResults = np.load(normalFormResultsFilename)
            normalFormVs = normalFormResults["vs"]
            normalFormTimes = normalFormResults["times"]

            iNapIKLine, = plt.plot(iNapIKTimes, iNapIKYs[0,:], color="r")
            normalFormLine, = plt.plot(normalFormTimes, normalFormVs, color="g")
            
#     plt.ylim((min(iNapIKYs[0,:]), max(iNapIKYs[0,:])))
    plt.ylabel("Voltage (mv)")
    plt.xlabel("Time (ms)")
    plt.figlegend([iNapIKLine, normalFormLine], ["INapIK", "Normal Form"], "upper right")
    plt.savefig(figFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

