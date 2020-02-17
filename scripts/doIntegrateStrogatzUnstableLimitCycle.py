
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from StrogatzUnstableLimitCycleModel import StrogatzUnstableLimitCycleModel

def main(argv):
    # mu = 1.0
    mu = -0.5
    w = 1.0
    b = 1.0
    r0 = 2.0
    theta0 = np.pi/6
    t0 = 0.0
    tf = 20.0
    dt = 1e-3
    traceCol = 'grey'
    traceMarker = '.'

    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    sULCModel = StrogatzUnstableLimitCycleModel(mu=mu, w=w, b=b)
    integrator = ode(sULCModel.deriv).set_integrator('vode', max_step=dt)

    y0 = np.array([r0, theta0])
    integrator.set_initial_value(y0, t0)
    ys = np.empty((2, nTSteps+1))
    ys[:, 0] = y0

    t = t0
    step = 0
    successfulIntegration = True
    while successfulIntegration and step<nTSteps:
        step = step+1
        """
        if step%100==0:
            print('Processing time %.05f out of %.02f' % (t, tf))
            sys.stdout.flush()
        """
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        times[step] = t
        ys[:, step] = y

    resultsFilename = 'results/integrationSULCModelMu%.02fR0%.02f.npz'%(mu, r0)
    np.savez(resultsFilename, times=times, ys=ys)

    rs = ys[0, :]
    thetas = ys[1, :]
    xs = rs*np.cos(thetas)
    ys = rs*np.sin(thetas)

    plt.plot(xs, ys, color=traceCol, marker=traceMarker)
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('figures/integrationSULCModelMu%.02f.eps'%mu)

    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

