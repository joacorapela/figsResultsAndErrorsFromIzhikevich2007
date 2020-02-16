
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel

def main(argv):
    i0 = 3.0
    v0 = -55.0
    n0 = 0.04
    tauV = lambda v: 0.152
    t0 = 0.0
    tf = 6.5
    dt = 1e-5
    resultsFilename = "results/integrationINapIKIExampleP163b_i0%.2fv0%.02f.npz"%(i0,v0)

    def i(t):
        return(i0)
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    htINapIKModel = INapIKModel.getHighThresholdInstance(i=i, 
                                                          tau=tauV);
    integrator = ode(htINapIKModel.deriv).set_integrator('vode', max_step=dt)

    y0 = np.array([v0, n0])
    integrator.set_initial_value(y0, t0)
    ys = np.empty((2, nTSteps+1))
    ys[:, 0] = y0

    t = t0
    step = 0
    successfulIntegration = True
    while successfulIntegration and step<nTSteps:
        step = step+1
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        if step%10000==0:
            print('Processed time %.05f out of %.02f: v=%02f, n=%02f' % (t, tf, y[0], y[1]))
            sys.stdout.flush()
        times[step] = t
        ys[:, step] = y

    np.savez(resultsFilename, times=times, ys=ys)

if __name__ == '__main__':
    main(sys.argv)

