
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
    y0 = 1.5
    t0 = 0.0
    tf = 15.0
    dt = 1e-5
    xBounds = [-10, 10]
    yBounds = [-10, 10]
    resultsFilename = "results/integrationA%fB%fC%fX0%fY0%f.npz"%(a, b, c, 
                                                                     x0, y0)
    def deriv(t, z):
        x = z[0]
        y = z[1]
        f = lambda x, y: a+x**2-y
        g = lambda x, y: b*x-c*y
        xDot = f(x=x, y=y)
        yDot = g(x=x, y=y)
        return(np.array([xDot, yDot]))

    integrator = ode(deriv).set_integrator('vode')

    z0 = np.array([x0, y0])
    integrator.set_initial_value(z0, t0)
    zs = [z0]
    times = [t0]

    step = 0
    t = t0
    z = z0
    successfulIntegration = True
    while successfulIntegration and t<tf and \
          xBounds[0]<=z[0] and z[0]<=xBounds[1] and\
          yBounds[0]<=z[1] and z[1]<=yBounds[1]:
        step = step + 1
        if step%10000==0:
            print('Processing time %.05f out of %.02f (%.02f, %.02f)' % (t, tf, z[0], z[1]))
            sys.stdout.flush()
        integrator.integrate(t+dt)
        t = integrator.t
        z = integrator.y
        times.append(t)
        zs.append(z.tolist())
    timesArray = np.array(times)
    zsArray = buildMatrixFromArraysList(arraysList=zs)

    np.savez(resultsFilename, times=timesArray, zs=zsArray)

if __name__ == '__main__':
    main(sys.argv)

