
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
    delta = -1e-2
    lMatrix = np.array([[1.0, 1.0], [-2.0, -1.0+delta]])
    def deriv(t, v):
        return(lMatrix.dot(v))
    vTracesCol = 'grey'

    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    vs = np.empty((2, nTSteps+1))
    t = t0
    step = 0
    vs[:, step] = v0
    successfulIntegration = True
    integrator = ode(deriv).set_integrator('vode')
    integrator.set_initial_value(v0, t0)
    while successfulIntegration and step<nTSteps:
        step = step+1
        """
        if step%100==0:
            print('Processing time %.05f out of %.02f' % (t, tf))
            sys.stdout.flush()
        """
        integrator.integrate(t+dt)
        t = integrator.t
        v = integrator.y
        times[step] = t
        vs[:,step] = v

    print(lMatrix)
    plt.plot(vs[0, :], vs[1, :], color=vTracesCol)
    plt.xlim((-3, 3))
    plt.ylim((-3, 3))
    plt.xlabel('u')
    plt.ylabel('w')
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

