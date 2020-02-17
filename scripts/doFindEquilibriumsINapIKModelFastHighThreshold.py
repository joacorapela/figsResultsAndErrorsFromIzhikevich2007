
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from myMath import findZeroByBisection

def main(argv):
    i0 = 3.0
    i = lambda v: i0
    c = 1.0
    eL = -80
    gL = 8.0
    gNa = 20.0
    gK = 10.0
    VoneHalf_m = -20.0
    k_m = 15.0
    VoneHalf_n = -25.0
    k_n = 5.0
    eNa = 60.0
    eK = -90
    tau = lambda v: 0.152
    ylim = (-100, 50)

    model = INapIKModel(i=i, c=c, gL=gL, eL=eL, gNa=gNa, eNa=eNa, 
                             gK=gK, eK=eK, 
                             mVOneHalf=VoneHalf_m, mK=k_m, 
                             nVOneHalf=VoneHalf_n, nK=k_n, 
                             tau=tau)
    vs = np.arange(start=-100, stop=50, step=.1)
    f = model.getFuncVDotAtNInf(i0=i0)

    plt.plot(vs, f(vs))
    plt.ylim(ylim)
    plt.xlabel('membrane potential, V (mV)')
    plt.ylabel('current (pA)')
    plt.grid()
    plt.show()

    vEq1 = findZeroByBisection(f, xMin=-70.0, xMax=-60.0)
    vEq2 = findZeroByBisection(f, xMin=-59.0, xMax=-55.0)
    vEq3 = findZeroByBisection(f, xMin=-40.0, xMax=-20.0)
    nEq1 = model._nInf(v=vEq1)
    nEq2 = model._nInf(v=vEq2)
    nEq3 = model._nInf(v=vEq3)

    print('fAtVEq1=%.04f, fAtVEq2=%.04f, fAtVEq3=%.04f)' % \
           (f(vEq1), f(vEq2), f(vEq3)))
    print('Eq1=(%.04f, %.04f), Eq2=(%.04f, %.04f), Eq3=(%.04f, %.04f)' % \
          (vEq1, nEq1, vEq2, nEq2, vEq3, nEq3))
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
