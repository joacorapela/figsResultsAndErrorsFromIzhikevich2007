
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel

def buildArrayFromList(aList):
    answer = np.empty((len(aList[0]), len(aList)))
    answer[:] = np.nan
    for i in xrange(len(aList)):
        answer[:,i] = aList[i]
    return(answer)

def main(argv):
    i0 = 40.0

    v0 = -60.00
    n0 = 0.0008
    t0 = 0.0
    t1 = 5.0
    tf = 40.0
    dt = 1e-5
    resultsFilenamePattern = 'results/integrationINapIKFig4-yyPulseStrength%d.npz'

    iPulseStrength = 0.0
    iPulseWidth = 1*dt
    def i(t):
        if t1-iPulseWidth/2<t and t<=t1+iPulseWidth/2:
            return(i0+iPulseStrength)
        return(i0)
    iNapIKModel = INapIKModel.getLowThresholdInstance(i=i)
    integrator = ode(iNapIKModel.deriv).set_integrator('vode', max_step=dt)

    y0 = [v0, n0]
    integrator.set_initial_value(y0, t0)
    ys = [y0]
    times = [t0]

    step = 0
    t = t0
    y = y0
    successfulIntegration = True
    while successfulIntegration and t<tf:
        step = step + 1
        if step%10000==0:
            print('Processing time %.05f out of %.02f (%.02f, %.02f)' % (t, tf, y[0], y[1]))
            sys.stdout.flush()
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        times.append(t)
        ys.append(y.tolist())
    timesArray = np.array(times)
    ysArray = buildArrayFromList(aList=ys)

    resultsFilename = resultsFilenamePattern%iPulseStrength
    np.savez(resultsFilename, times=timesArray, ys=ysArray)

if __name__ == '__main__':
    main(sys.argv)

