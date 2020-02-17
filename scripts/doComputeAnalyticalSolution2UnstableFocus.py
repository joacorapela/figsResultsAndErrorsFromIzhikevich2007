
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
    l = np.array([[1.0/4, 1.0],[-3.0/2, 1.0/4]])
    vTracesCol = 'grey'

    detL = l[0, 0]*l[1, 1]-l[1, 0]*l[0, 1]
    lInv = np.array([[l[1, 1], -l[1, 0]], [-l[0, 1], l[0, 0]]])/detL
    a0s = lInv.dot(v0)

    eigRes = np.linalg.eig(l)
    realEvals = eigRes[0][0].real
    imagEvals = eigRes[0][0].imag
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
        v = np.exp(realEvals*t)*(a0s[0]*np.exp(1j*imagEvals*t)*eigRes[1][:, 0]+\
                                 a0s[1]*np.exp(-1j*imagEvals*t)*eigRes[1][:, 1])
        times[step] = t
        vs[:,step] = v.real

    plt.plot(vs[0, :], vs[1, :], color=vTracesCol)
    plt.xlabel('u')
    plt.ylabel('w')
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

