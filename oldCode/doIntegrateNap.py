
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from NapModel import NapModel

def main(argv):
    i0 = -800
    v00 = -120
    v0f = 40
    dv0 = 5
    t0 = 0.0
    tf = 2.0
    dt = 1e-5
    vTracesCol = 'grey'

    def i(t): return(i0)
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    napModel = NapModel(i=i)
    integrator = ode(napModel.deriv).set_integrator('vode')

    for v0 in xrange(v00, v0f+dv0, dv0):
        print('Processing v0=%.2f' % v0)
        integrator.set_initial_value(v0, t0)
        vs = np.empty(nTSteps+1)

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
            v = integrator.y
            times[step] = t
            vs[step] = v

        plt.plot(times, vs, color=vTracesCol)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (mV)')
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

