
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode

def main(argv):
    v_sn = -60.9325
    i_sn = 4.51
    a = .1887
    c = 1
    i0 = i_sn-5
    vEqStable = v_sn-np.sqrt(-c/a*(i0-i_sn))
    vEqUnstable = v_sn+np.sqrt(-c/a*(i0-i_sn))
    vStep = 2
    deltaV = .5
    v0From = vEqStable - 5*vStep
    v0To = vEqUnstable-deltaV
    t0 = 0.0
    tf = 1.3
    dt = 1e-5
    vTracesCol = 'grey'

    v0s = np.append(np.arange(v0From, v0To, vStep), vEqUnstable+deltaV)

    def deriv(t, v):
        deriv = c*(i0-i_sn)+a*(v-v_sn)**2
        return(deriv)
        
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    integrator = ode(deriv).set_integrator('vode', nsteps=1000)

    for v0 in v0s:
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
    plt.axhline(y=vEqStable, color="b")
    plt.axhline(y=vEqUnstable, color="b")
    plt.axhline(y=v_sn, color="r")
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (mV)')
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

