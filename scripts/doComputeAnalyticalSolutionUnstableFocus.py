
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from KirModel import KirModel

def main(argv):
    t0 = 0.0
    tf = 20.0
    dt = 1e-2
    v0 = np.array([1.0, 0.0])
    vTracesCol = 'grey'

    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    vs = np.empty((2, nTSteps+1))
    t = t0
    step = 0
    vs[:, step] = v0
    while step<nTSteps:
        step = step+1
        """
        if step%100==0:
            print('Processing time %.05f out of %.02f' % (t, tf))
            sys.stdout.flush()
        """
        t = t + dt
        v = np.sqrt(5.0/2)*np.exp(t/4)*\
            np.array([np.cos(np.sqrt(6.0)/2*t)*np.sqrt(2.0/5),\
                      -np.sin(np.sqrt(6.0)/2*t)*np.sqrt(3.0/5)])
        times[step] = t
        vs[:,step] = v

    plt.plot(vs[0, :], vs[1, :], color=vTracesCol)
    plt.xlabel('u')
    plt.ylabel('w')
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

