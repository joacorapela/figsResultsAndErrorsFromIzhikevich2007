

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField
from HodgkinAndHuxleyModel import HodgkinAndHuxleyModel

def main(argv):
    figFilename = "figures/fig2-13.eps"

    def i(t):
        return 0.0

    hhModel = HodgkinAndHuxleyModel(i=i)
    v = np.arange(-40, 100, .1)
    nInf = hhModel._nInf(v=v)
    mInf = hhModel._mInf(v=v)
    hInf = hhModel._hInf(v=v)
    tauN = hhModel._tauN(v=v)
    tauM = hhModel._tauM(v=v)
    tauH = hhModel._tauH(v=v)

    f, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot(v, nInf, label=r"$n_\infty$(V)")
    ax1.plot(v, mInf, label=r"$m_\infty$(V)")
    ax1.plot(v, hInf, label=r"$h_\infty$(V)")
    ax1.legend(loc="lower right")
    ax1.set_xlabel("V (mv)")
    ax1.set_ylabel("Probability")

    ax2.plot(v, tauN, label=r"$\tau_n$(V)")
    ax2.plot(v, tauM, label=r"$\tau_m$(V)")
    ax2.plot(v, tauH, label=r"$\tau_h$(V)")
    ax2.legend(loc="upper right")
    ax2.set_xlabel("V (mv)")
    ax2.set_ylabel("Time (ms)")

    plt.savefig(figFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

