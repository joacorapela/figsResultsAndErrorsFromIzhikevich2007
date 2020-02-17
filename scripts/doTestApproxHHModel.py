
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from HodgkinAndHuxleyModel import HodgkinAndHuxleyModel
from ApproxHodgkinAndHuxleyModel import ApproxHodgkinAndHuxleyModel


def main(argv):
    vs = np.arange(-40, 100, .1)
    hhModel = HodgkinAndHuxleyModel(i=None)
    approxHHModel = ApproxHodgkinAndHuxleyModel(i=None)
    nInfs = hhModel._nInf(v=vs)
    approxNInfs = approxHHModel._nInf(v=vs)
    mInfs = hhModel._mInf(v=vs)
    approxMInfs = approxHHModel._mInf(v=vs)
    hInfs = hhModel._hInf(v=vs)
    approxHInfs = approxHHModel._hInf(v=vs)
    tauNs = hhModel._tauN(v=vs)
    approxTauNs = approxHHModel._tauN(v=vs)
    tauMs = hhModel._tauM(v=vs)
    approxTauMs = approxHHModel._tauM(v=vs)
    tauHs = hhModel._tauH(v=vs)
    approxTauHs = approxHHModel._tauH(v=vs)

    plt.subplot(2, 1, 1)
    plt.plot(vs, nInfs, label=r"$n_\infty$(v)")
    plt.plot(vs, approxNInfs, label=r"$\tilde{n}_\infty$(v)")
    plt.plot(vs, mInfs, label=r"$m_\infty$(v)")
    plt.plot(vs, approxMInfs, label=r"$\tilde{m}_\infty$(v)")
    plt.plot(vs, hInfs, label=r"$h_\infty$(v)")
    plt.plot(vs, approxHInfs, label=r"$\tilde{h}_\infty$(v)")
    plt.ylabel("Proability Open")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(vs, tauNs, label=r"$\tau_n$(v)")
    plt.plot(vs, approxTauNs, label=r"$\hat{\tau}_n$(v)")
    plt.plot(vs, tauMs, label=r"$\tau_m$(v)")
    plt.plot(vs, approxTauMs, label=r"$\hat{\tau}_m$(v)")
    plt.plot(vs, tauHs, label=r"$\tau_h$(v)")
    plt.plot(vs, approxTauHs, label=r"$\hat{\tau}_h$(v)")
    plt.xlabel("Voltage (mV)")
    plt.ylabel("Time Constant")
    plt.legend()

    plt.show()

if __name__ == '__main__':
    main(sys.argv)

