
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel
from utils import buildMatrixFromArraysList

def main(argv):
    v0 = -65.00
    n0 = 0.0008
    t0 = 0.0
    tf = 140.0
    current0 = 0.0
    currentf = 30.0
    dt = 1e-3
    resultsFilename = 'results/integrationINapIKFig4-33.npz'

    iSlope = 30.0/100.0
    def i(t, iSlope=iSlope):
        return(current0+iSlope*t)
    iNapIKModel = INapIKModel.getLowThresholdInstance(i=i)
    integrator = ode(iNapIKModel.deriv).set_integrator('vode', max_step=dt)
    # integrator = ode(iNapIKModel.deriv).set_integrator('vode')

    y0 = [v0, n0]
    integrator.set_initial_value(y0, t0)
    ys = [y0]
    times = [t0]
    currents = [i(t0)]

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
        currents.append(i(t))
    timesArray = np.array(times)
    ysArray = buildMatrixFromArraysList(arraysList=ys)
    currentsArray = np.array(currents)
    np.savez(resultsFilename, times=timesArray, ys=ysArray,
                              currents=currentsArray)

if __name__ == '__main__':
    main(sys.argv)

