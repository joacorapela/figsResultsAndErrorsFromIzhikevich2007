
# For the estimation of the parameter of tauM see doProblem2-4_tauM.py

import sys
import numpy as np
import matplotlib.pyplot as plt
from HodgkinAndHuxleyModel import HodgkinAndHuxleyModel
import pdb

def main(argv):
    hhModel = HodgkinAndHuxleyModel(i=None)
    vs = np.arange(-40, 100, 1e-3)

    nInfs = hhModel._nInf(v=vs)
    nVOneHalf = vs[np.argmin(np.abs(nInfs-.5))]
    nK = -(vs[np.argmin(np.abs(nInfs-1.0/(1+np.exp(1))))]-nVOneHalf)
    nInfsApproxFunc = lambda v: 1.0/(1+np.exp((nVOneHalf-v)/nK))
    nInfsApprox = nInfsApproxFunc(v=vs)

    mInfs = hhModel._mInf(v=vs)
    mVOneHalf = vs[np.argmin(np.abs(mInfs-.5))]
    mK = -(vs[np.argmin(np.abs(mInfs-1.0/(1+np.exp(1))))]-mVOneHalf)
    mInfsApproxFunc = lambda v: 1.0/(1+np.exp((mVOneHalf-v)/mK))
    mInfsApprox = mInfsApproxFunc(v=vs)

    hInfs = hhModel._hInf(v=vs)
    hVOneHalf = vs[np.argmin(np.abs(hInfs-.5))]
    hK = -(vs[np.argmin(np.abs(hInfs-1.0/(1+np.exp(1))))]-hVOneHalf)
    hInfsApproxFunc = lambda v: 1.0/(1+np.exp((hVOneHalf-v)/hK))
    hInfsApprox = hInfsApproxFunc(v=vs)

    tauNs = hhModel._tauN(v=vs)
    nCBase = min(tauNs)
    nCAmp = max(tauNs)-nCBase
    nVMax = vs[np.argmax(tauNs)]
    nSigma = abs(nVMax-vs[np.argmin(abs((tauNs-nCBase)-(max(tauNs)-nCBase)*np.exp(-1)))])
    tauNsApproxFun = lambda v: nCBase+nCAmp*np.exp(-(nVMax-v)**2/nSigma**2)
    tauNsApprox = tauNsApproxFun(v=vs)

#     tauMs = hhModel._tauM(v=vs)
#     mCBase = min(tauMs)
#     mCAmp = max(tauMs)-mCBase
#     mVMax = vs[np.argmax(tauMs)]
#     mSigma = abs(mVMax-vs[np.argmin(abs((tauMs-mCBase)-(max(tauMs)-mCBase)*np.exp(-1)))])
#     tauMsApproxFun = lambda v: mCBase+mCAmp*np.exp(-(mVMax-v)**2/mSigma**2)
#     tauMsApprox = tauMsApproxFun(v=vs)

    # begin delete
    refValue = mCBase+mCAmp*np.exp(-1)
    tauMAtMVMaxPlusMSigma = hhModel._tauN(v=mVMax+mSigma)
    tauMApproxAtMVMaxPlusMSigma = tauMsApproxFun(v=mVMax+mSigma)
    closeToZero1 = abs(tauMAtMVMaxPlusMSigma-refValue)
    closeToZero2 = abs(tauMApproxAtMVMaxPlusMSigma-refValue)
    pdb.set_trace()
    # end delete

    tauHs = hhModel._tauH(v=vs)
    hCBase = min(tauHs)
    hCAmp = max(tauHs)-hCBase
    hVMax = vs[np.argmax(tauHs)]
    hSigma = abs(hVMax-vs[np.argmin(abs((tauHs-hCBase)-(max(tauHs)-hCBase)*np.exp(-1)))])
    tauHsApproxFun = lambda v: hCBase+hCAmp*np.exp(-(hVMax-v)**2/hSigma**2)
    tauHsApprox = tauHsApproxFun(v=vs)

    plt.plot(vs, nInfs, label=r"$n_{\infty}$(v)")
    plt.plot(vs, nInfsApprox, label=r"$\hat{n}_{\infty}$(v)")
    plt.plot(vs, mInfs, label=r"$m_{\infty}$(v)")
    plt.plot(vs, mInfsApprox, label=r"$\hat{m}_{\infty}$(v)")
    plt.plot(vs, hInfs, label=r"$h_{\infty}$(v)")
    plt.plot(vs, hInfsApprox, label=r"$\hat{h}_{\infty}$(v)")
    plt.xlabel("V (mv)")
    plt.ylabel("Probability")
    plt.legend(loc="lower right")

    plt.figure()
    plt.plot(vs, tauNs, label=r"$\tau_N$(v)")
    plt.plot(vs, tauNsApprox, label=r"$\hat{\tau}_N$(v)")
#     plt.plot(vs, tauMs, label=r"$\tau_M$(v)")
#     plt.plot(vs, tauMsApprox, label=r"$\hat{\tau}_M$(v)")
    plt.plot(vs, tauHs, label=r"$\tau_H$(v)")
    plt.plot(vs, tauHsApprox, label=r"$\hat{\tau}_H$(v)")
    plt.xlabel("V (mv)")
    plt.ylabel("Time Constant")
    plt.legend(loc="upper right")

    plt.show()
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
