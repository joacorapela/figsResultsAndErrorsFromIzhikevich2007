

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField

def main(argv):
    resultsFilename = "results/integrationHodgkinAndHuxley_noInput.npz"
    figFilename = "figures/figHH_noInput.eps"

    gL = 0.3
    gNaMax = 120.0
    gKMax = 36.0
    eL = 10.6 
    eNa = 120.0
    eK = -12.0

    results = np.load(resultsFilename)
    ys = results["ys"]
    times = results["times"]
    inputCurrent = results["inputCurrent"]
    vs = ys[0,:]
    ns = ys[1,:]
    ms = ys[2,:]
    hs = ys[3,:]

    plt.figure(figsize=(12, 12))

    ax1 = plt.subplot2grid((7,1), (0,0), rowspan=3)
    ax2 = plt.subplot2grid((7,1), (3,0))
    ax3 = plt.subplot2grid((7,1), (4,0))
    ax4 = plt.subplot2grid((7,1), (5,0))
    ax5 = plt.subplot2grid((7,1), (6,0))

    ax1.plot(times, vs, label="V(t)")
    ax1.legend(loc="upper left")
    ax1.grid()

    ax2.plot(times, ns, label="n(t)")
    ax2.plot(times, ms, label="m(t)")
    ax2.plot(times, hs, label="h(t)")
    ax2.legend(loc="upper left")

    gNa = gNaMax*pow(ms, 3)*hs
    gK = gKMax*pow(ns, 4) 
    ax3.plot(times, gNa, label=r"$g_{Na}$(t)")
    ax3.plot(times, gK, label=r"$g_K$(t)")
    ax3.legend(loc="upper left")

    iL = gL*(vs-eL)
    iNa = gNaMax*pow(ms, 3)*hs*(vs-eNa)
    iK = gKMax*pow(ns, 4)*(vs-eK)
    ax4.plot(times, iNa, label=r"$I_{Na}$(t)")
    ax4.plot(times, iK, label=r"$I_K$(t)")
    ax4.plot(times, iNa+iK+iL, label=r"$I_{Na}+I_K+I_L$")
    ax4.legend(loc="upper left")

    ax5.plot(times, inputCurrent, label="I(t)")
    ax5.set_xlabel("Time (ms)")
    ax5.set_ylim((0, 35))
    ax5.legend(loc="upper left")

    plt.savefig(figFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

