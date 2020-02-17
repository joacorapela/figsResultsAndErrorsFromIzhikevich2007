
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from KirModel import KirModel

def main(argv):
    t0 = 0.0
    tf = 400.0
    dt = 1e-2
    v0 = np.array([1.0, 0.0])
    delta =  +1e-2
    lMatrix = np.array([[1.0, 1.0],[-2.0, -1.0+delta]])
    vTracesCol = 'grey'

    detLMatrix = lMatrix[0, 0]*lMatrix[1, 1]-lMatrix[1, 0]*lMatrix[0, 1]
    lInv = np.array([[lMatrix[1, 1], -lMatrix[1, 0]], [-lMatrix[0, 1], lMatrix[0, 0]]])/detLMatrix
    a0s = lInv.dot(v0)

    eigRes = np.linalg.eig(lMatrix)
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

    print(lMatrix)
    plt.plot(vs[0, :], vs[1, :], color=vTracesCol)
    plt.axvline(color=vTracesCol)
    plt.axhline(color=vTracesCol)
    plt.xlabel('u')
    plt.ylabel('w')
    plt.xlim((-3, 3))
    plt.ylim((-3, 3))
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

