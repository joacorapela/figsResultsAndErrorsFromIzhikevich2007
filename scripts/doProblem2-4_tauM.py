
import sys
import numpy as np
import matplotlib.pyplot as plt
from HodgkinAndHuxleyModel import HodgkinAndHuxleyModel
import pdb

def main(argv):
    hhModel = HodgkinAndHuxleyModel(i=None)
    vs = np.arange(10, 100, 1e-3)

    tauMs = hhModel._tauM(v=vs)
    mCBase = min(tauMs)
    mCAmp = max(tauMs)-mCBase
    mVMax = vs[np.argmax(tauMs)]
    mSigma = abs(mVMax-vs[np.argmin(abs((tauMs-mCBase)-(max(tauMs)-mCBase)*np.exp(-1)))])
    tauMsApproxFun = lambda v: mCBase+mCAmp*np.exp(-(mVMax-v)**2/mSigma**2)
    tauMsApprox = tauMsApproxFun(v=vs)

    # begin delete
    refValue = mCBase+mCAmp*np.exp(-1)
    tauMAtMVMaxPlusMSigma = hhModel._tauN(v=mVMax+mSigma)
    tauMApproxAtMVMaxPlusMSigma = tauMsApproxFun(v=mVMax+mSigma)
    closeToZero1 = abs(tauMAtMVMaxPlusMSigma-refValue)
    closeToZero2 = abs(tauMApproxAtMVMaxPlusMSigma-refValue)
    # end delete

    plt.figure()
    plt.plot(vs, tauMs, label=r"$\tau_M$(v)")
    plt.plot(vs, tauMsApprox, label=r"$\hat{\tau}_M$(v)")
    plt.axhline(y=min(tauMs[vs>60]))
    plt.xlabel("V (mv)")
    plt.ylabel("Time Constant")
    plt.legend(loc="upper right")

    plt.show()
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
