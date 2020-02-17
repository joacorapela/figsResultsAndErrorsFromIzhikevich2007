
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel

def main(argv):
    i0 = 0
    v0 = -61.0
    n0 = 0.04
    t0 = 0.0
    t1 = 1.0
    tf = 6.5
    dt = 1e-5
    eL = -78.0 
    nVOneHalf = -45.0, 
    iPulseStrength = 5000000
    iPulseWidth = 1*dt
    traceCol = 'grey'
    traceMarker = '.'

    def i(t):
        if t1-iPulseWidth/2<t and t<=t1+iPulseWidth/2:
            return(i0+iPulseStrength)
        return(i0)
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    ltINapIKModel = INapIKModel(i=i, eL=eL, nVOneHalf=nVOneHalf)
    integrator = ode(ltINapIKModel.deriv).set_integrator('vode', max_step=dt)

    y0 = np.array([v0, n0])
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

    resultsFilename = 'results/integrationINapIKIPulseStrength%d.npz'%iPulseStrength
    np.savez(resultsFilename, times=times, ys=ys)

    plt.plot(ys[0, :], ys[1, :], color=traceCol, marker=traceMarker)
    plt.grid()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.savefig('figures/phaseSpaceIntegrationINapIKIPulseStrength%d.eps'%iPulseStrength)
    plt.figure()
    plt.plot(times, ys[0, :])
    plt.grid()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig('figures/voltageTraceIntegrationINapIkKPulseStrength%d.eps'%iPulseStrength)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

