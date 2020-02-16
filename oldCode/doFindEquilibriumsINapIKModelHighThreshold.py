
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from myMath import findZeroByBisection

def main(argv):
    if len(argv)==1:
        i0 = 0.0
    else:
        i0 = float(argv[1])
    i = lambda v: i0
    ylim = (-100, 100)

    model = INapIKModel.getHighThresholdInstance(i=i)
    vs = np.arange(start=-100, stop=50, step=.1)
    f = model.getFuncVDotAtNInf(i0=i0)

    plt.plot(vs, f(vs))
    plt.ylim(ylim)
    plt.xlabel('membrane potential, V (mV)')
    plt.ylabel('current (pA)')
    plt.grid()
    plt.show()
    pdb.set_trace()

    vEq1 = findZeroByBisection(f, xMin=-60.9, xMax=-60.7)
    vEq2 = findZeroByBisection(f, xMin=-60.0, xMax=-40.0)
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
