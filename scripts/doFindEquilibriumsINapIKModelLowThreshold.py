
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from myMath import findZeroByBisection

def main(argv):
    ylim = (-100, 50)

    model = INapIKModel.getLowThresholdInstance(i=None)
    vs = np.arange(start=-100, stop=50, step=.1)
    f = model.getFuncVDotAtNInf(i0=0.0)

    plt.plot(vs, f(vs))
    plt.ylim(ylim)
    plt.xlabel('membrane potential, V (mV)')
    plt.ylabel('current (pA)')
    plt.grid()
    plt.show()

    pdb.set_trace()    
    vEq1 = findZeroByBisection(f, xMin=-70.0, xMax=-50.0)
    nEq1 = model._nInf(v=vEq1)

    print('Eq1=(%.02f, %.02f)' % (vEq1, nEq1))

if __name__=="__main__":
    main(sys.argv)
