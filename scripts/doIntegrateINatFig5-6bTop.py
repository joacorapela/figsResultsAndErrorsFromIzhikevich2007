
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INatModel import INatModel

def main(argv):
    if len(argv)!=2:
        print("Usage %s <v0>"%argv[0])
        return

    v0 = float(argv[1])
    i0 = 0.0
    # v0 = -65.7
    # v0 = -60.0
    h0 = 0.63
    t0 = 0.0
    tf = 100.0
    dt = 1e-3
    traceCol = 'grey'
    traceMarker = '.'

    def i(t):
        return(i0)
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    iNatModel = INatModel.getLowThresholdInstance(i=i)
    integrator = ode(iNatModel.deriv).set_integrator('vode', max_step=dt)

    y0 = np.array([v0, h0])
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

    resultsFilename = 'results/integrationINatFig5-6bTopV0%.2f.npz'%v0
    np.savez(resultsFilename, times=times, ys=ys)

    plt.plot(ys[0, :], ys[1, :], color=traceCol, marker=traceMarker)
    plt.gca().invert_yaxis()
    plt.grid()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('Na inactivation, h')
    plt.savefig('figures/phaseSpaceIntegrationINatFig5-6aTopV0%.2f.eps'%v0)
    plt.figure()
    plt.plot(times, ys[0, :])
    plt.grid()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig('figures/voltageTraceIntegrationINatFig5-6aTopV0%.2f.eps'%v0)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

