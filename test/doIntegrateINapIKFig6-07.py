
import sys
import numpy as np
from scipy.integrate import ode
from INapIKModel import INapIKModel

def main(argv):
    if len(argv)!=3:
        sys.exit("Usage: %s tauV i0"%argv[0])
    i0 = float(argv[2])
    aTauV = float(argv[1])
    tauV = lambda v: aTauV

    v0 = -60.9325
    t0 = 0.0
    tf = 100.0
    dt = 1e-3
    resultsFilename = 'results/integrationINapIKFig6-07TauV%.02fI%.02f.npz'%(aTauV, i0)

    iPulseWidth = 1*dt
    def i(t):
        return(i0)
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    iNapIKModel = INapIKModel.getHighThresholdInstance(i=i, tau=tauV)
    integrator = ode(iNapIKModel.deriv).set_integrator('vode', max_step=dt)

    y0 = np.array([v0, iNapIKModel._nInf(v=v0)])
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

    np.savez(resultsFilename, i0=i0, times=times, ys=ys)

if __name__ == '__main__':
    main(sys.argv)

