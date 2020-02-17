
import sys
import numpy as np
import pdb
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel

def main(argv):
    # i0 = 1000
    # i0 = 0
    i0 = 40
    # v0 = -60.86
    v0 = -45.0
    n0 = 0.07
    t0 = 0.0
    tf = 20.0
    dt = 1e-3
    eL = -78.0 
    nVOneHalf = -45.0, 
    resultsFilenamePattern = 'results/integrationINapIKStepsize%d.npz'

    def i(t):
        return(i0)
    ltINapIKModel = INapIKModel.getLowThresholdInstance()
    ltINapIKModel.setI(i=i)
    integrator = ode(ltINapIKModel.deriv).set_integrator('vode', max_step=dt)

    nTSteps = round((tf-t0)/dt)
    y0 = np.array([v0, n0])
    integrator.set_initial_value(y0, t0)
    ys = np.empty((2, nTSteps+1))
    ys[:, 0] = y0
    t = t0
    step = 0
    successfulIntegration = True
    times = np.empty(nTSteps+1)
    while successfulIntegration and step<nTSteps:
        step = step+1
        if step%100==0:
            print('Processing time %.05f out of %.02f' % (t, tf))
            sys.stdout.flush()
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        times[step] = t
        ys[:, step] = y

    resultsFilename = resultsFilenamePattern%i0
    np.savez(resultsFilename, times=times, ys=ys)

if __name__ == '__main__':
    main(sys.argv)

