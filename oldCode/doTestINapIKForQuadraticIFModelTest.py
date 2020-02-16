
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel

def main(argv):
    i0 = 7.0
    vSN = -60.9325
    v0 = vSN
    n0 = 0.0004
    t0 = 0.0
    tf = 15.0
    dt = 1e-5
    resultsFilename = 'results/iNapIKModelIntegrationForQuadraticIFTest.npz'

    def i(t):
        return(i0)
    iNapIKModel = INapIKModel.getHighThresholdInstance(i=i)
    integrator = ode(iNapIKModel.deriv).set_integrator('vode')

    y0 = np.array([v0, n0])
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
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

    np.savez(resultsFilename, times=times, ys=ys)

    plt.plot(times, ys[1,:])
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Voltage (mV)")
    plt.show()

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
