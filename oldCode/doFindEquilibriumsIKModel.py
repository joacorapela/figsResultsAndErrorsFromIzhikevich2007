
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from IKModel import IKModel
from myMath import findZeroByBisection

def main(argv):
    if len(argv)==1:
        i0 = 0.0
    else:
        i0 = float(argv[1])
    i = lambda v: i0
    c = 1.0
    gL = 1.0
    eL = -80.0
    gK = 1.0
    eK = -90.0
    mVOneHalf = -53.0
    mK = 15.0
    tau = lambda v: 1.0
    ylim = (-100, 100)

    model = IKModel(i=i, c=c, gL=gL, eL=eL, gK=gK, eK=eK, 
                         mVOneHalf=mVOneHalf, mK=mK, tau=tau)
    vs = np.arange(start=-100, stop=50, step=.1)
    f = model.getFuncVDotAtMInf(i0=i0)

    plt.plot(vs, f(vs))
    plt.ylim(ylim)
    plt.xlabel('membrane potential, V (mV)')
    plt.ylabel('current (pA)')
    plt.grid()
    plt.show()

    vEq = findZeroByBisection(f, xMin=-100.0, xMax=-60.0)
    mEq = model._mInf(v=vEq)

    print('fAtVEq=%.04f' % (f(vEq)))
    print('vEq=%.04f, mEq=%.04f' % (vEq, mEq))
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
