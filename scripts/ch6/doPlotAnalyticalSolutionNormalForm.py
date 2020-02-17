
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
    tf = 3.4
    dt = 1e-5
    vTracesCol = 'grey'

    v0s = np.append(np.arange(v0From, v0To, vStep), vEqUnstable+deltaV)
    times = np.arange(t0, tf, dt);
    k = c*(i0-i_sn)
    sqrtFactor = np.sqrt(abs(a/k))
    nTSteps = round((tf-t0)/dt)

    def getConstantForV0(v0):
        return(np.arctanh((v0-v_sn)*sqrtFactor))

    for v0 in v0s:
        print('Processing v0=%.2f' % v0)
        constant = getConstantForV0(v0=v0)
        vs = v_sn+1/sqrtFactor*np.tanh(k*sqrtFactor*times+constant)
        pdb.set_trace()
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

