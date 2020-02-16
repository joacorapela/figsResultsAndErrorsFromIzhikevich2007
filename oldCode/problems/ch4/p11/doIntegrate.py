
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from utils import buildMatrixFromArraysList

def main(argv):
    a = 7.0/8.0
    b = 2.0
    c = 1.0
    x0 = 0.6
    y0 = 1.2
    t0 = 0.0
    tf = 15.0
    dt = 1e-5
    resultsFilenamePattern = "results/integrationA%fB%fC%fX0%fY0%f.npz"%\
                              (a, b, c, x0, y0)
    def deriv(self, t, y):
        x = y[0]
        y = y[1]
        f = lambda x, y: a+x**2-y
        g = lambda x, y: b*x-c*y
        xDot = f(x=x, y=y)
        yDot = f(x=x, y=y)
        return(np.array([xDot, yDot]))

    integrator = ode(deriv).set_integrator('vode')

    y0 = np.array([x0, y0])
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
    ysArray = buildMatrixFromArraysList(arraysList=ys)

    np.savez(resultsFilename, times=timesArray, ys=ysArray)

if __name__ == '__main__':
    main(sys.argv)

