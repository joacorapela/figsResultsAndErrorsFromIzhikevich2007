
import sys
import pdb
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateModelForward

def main(argv):
    resultsFilename = 'results/integrationINapIKFig10_4LeftPanel_INapIKLowThreshold.npz'
    figFilename = 'figures/fig10_4LeftPanel_INapIKLowThreshold.eps'

    results = np.load(resultsFilename)
    plt.plot(results["timesDC"], results["ysDC"][0,:], label="DC")
    plt.plot(results["timesDCPulse"], results["ysDCPulse"][0,:], label="Pulse")
    # plt.axvline(x=tPulse, color="red")
    plt.legend(loc="lower right")
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane Potential (mV)")
    plt.savefig(figFilename)
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

