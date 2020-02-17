
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
    resultsFilename = "results/integrationINapIKFig10_10_matching1-1Sync.npz"
    figFilenamePattern = "figures/fig10_10a_matching1-1SyncXlimFrom%.02fTo%.02f.eps"
    xlimEarly = (40.0, 80.0)
    xlimLate = (240.0, 280.0)

    earlyFigFilename = figFilenamePattern%xlimEarly
    lateFigFilename = figFilenamePattern%xlimLate

    results = np.load(resultsFilename)

    plt.plot(results["timesDCTrainPulses"], results["ysDCTrainPulses"][0,:], color="blue")
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane Potential (mV)")
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(results["timesDCTrainPulses"], results["i"], color="lightgray")
    ax2.set_ylabel("Input Current (mA)")
    plt.xlim(xlimEarly)
    plt.savefig(earlyFigFilename)
    plt.xlim(xlimLate)
    plt.savefig(lateFigFilename)
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

