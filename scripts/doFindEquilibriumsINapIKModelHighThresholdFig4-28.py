
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from myMath import findZeroByBisection

def main(argv):
    if len(argv)==1:
        i0 = 4.512865
    else:
        i0 = float(argv[1])
    i = lambda v: i0
    ylim = (-100, 100)

    model = INapIKModel.getHighThresholdInstance(i=i)
    # vs = np.arange(start=-100, stop=50, step=.1)
    vs = np.arange(start=-60.935, stop=-60.925, step=.0001)
    f = model.getFuncVDotAtNInf(i0=i0)

    plt.plot(vs, f(vs))
    # plt.ylim(ylim)
    plt.xlabel('membrane potential, V (mV)')
    plt.ylabel(r'$\dot{v}$')
    plt.axhline(y=0, color="black")
    plt.grid()
    plt.show()
    pdb.set_trace()

    vEq1 = findZeroByBisection(f, xMin=-61.10, xMax=-61.00)
    nEq1 = model._nInf(v=vEq1)

    print('fAtVEq1=%.04f)' % (f(vEq1)))
    print('Eq1=(%.04f, %.04f)' % (vEq1, nEq1))
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
