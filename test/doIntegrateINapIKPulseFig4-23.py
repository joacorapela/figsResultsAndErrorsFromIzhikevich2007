
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel

def main(argv):
    i0 = 3.0
    tauV = lambda v: 0.152

    v0 = -63.8054
    n0 = 0.0004
    t0 = 0.0
    t1 = 5.0
    tf = 15.0
    dt = 1e-5
    resultsFilenamePattern = 'results/integrationINapIKFig4-23PulseStrength%d.npz'

    iPulseStrength = 1000000
    iPulseWidth = 1*dt
    def i(t):
        if t1-iPulseWidth/2<t and t<=t1+iPulseWidth/2:
            return(i0+iPulseStrength)
        return(i0)
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    iNapIKModel = INapIKModel.getHighThresholdInstance(i=i, tau=tauV)
    integrator = ode(iNapIKModel.deriv).set_integrator('vode', max_step=dt)

    y0 = np.array([v0, n0])
    integrator.set_initial_value(y0, t0)
    ys = np.empty((2, nTSteps+1))
    ys[:, 0] = y0

    t = t0
    step = 0
    successfulIntegration = True
    while successfulIntegration and step<nTSteps:
        step = step+1
        if step%100000==0:
            print('Processing time %.05f out of %.02f' % (t, tf))
            sys.stdout.flush()
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        times[step] = t
        ys[:, step] = y

    resultsFilename = resultsFilenamePattern%iPulseStrength
    np.savez(resultsFilename, times=times, ys=ys)

if __name__ == '__main__':
    main(sys.argv)

