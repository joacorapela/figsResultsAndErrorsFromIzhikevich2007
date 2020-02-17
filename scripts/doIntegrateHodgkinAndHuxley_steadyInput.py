
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from HodgkinAndHuxleyModel import HodgkinAndHuxleyModel

def main(argv):
    hhModel = HodgkinAndHuxleyModel(i=None)
    v0 = 5.0
    i0 = hhModel._gL*(v0-hhModel._eL)+\
         hhModel._gKMax*pow(hhModel._nInf(v=v0),4)*(v0-hhModel._eK)+\
         hhModel._gNaMax*pow(hhModel._mInf(v=v0),3)*hhModel._hInf(v=v0)*\
          (v0-hhModel._eNa)
    pdb.set_trace()
    # n0 = 0.31767691406070614
    # m0 = 0.052932485257253123
    # h0 = 0.5961207535084404
    n0 = 0.32
    m0 = 0.05
    h0 = 0.60
    t0 = 0.0
    t1 = 2.0
    t2 = 10.0
    tf = 20.0
    dt = 1e-3
    nVOneHalf = -45.0, 
    iPulse1Strength = 10.0
    iPulse2Strength = 25.0
    iPulseWidth = 0.25
    traceCol = 'grey'
    traceMarker = '.'

    def i(t):
        return(i0)
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    hhModel = HodgkinAndHuxleyModel(i=i)
    integrator = ode(hhModel.deriv).set_integrator('vode', max_step=dt)
#     integrator = ode(hhModel.deriv).set_integrator('vode')

    y0 = np.array([v0, n0, m0, h0])
    integrator.set_initial_value(y0, t0)
    ys = np.empty((4, nTSteps+1))
    ys[:, 0] = y0

    t = t0
    step = 0
    successfulIntegration = True
    while successfulIntegration and step<nTSteps:
        step = step+1
        if step%1000==0:
            print('Processing time %.05f out of %.02f' % (t, tf))
            sys.stdout.flush()
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        times[step] = t
        ys[:, step] = y

    inputCurrent = np.empty(len(times))
    for j in xrange(len(times)):
        inputCurrent[j] = i(t=times[j])
    resultsFilename = 'results/integrationHodgkinAndHuxley_steadyInput%.02f.npz'%(i0)
    np.savez(resultsFilename, times=times, ys=ys, inputCurrent=inputCurrent)

    plt.plot(times, ys[0, :])
    plt.grid()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)') 
    plt.savefig('figures/voltageTraceIntegrationHodgkinAndHuxley_steadyInput%.02f.eps'%(i0))
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

