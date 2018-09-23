

import sys
import numpy as np
import pdb
# from scipy.integrate import ode
# from scipy.integrate import odeint
import matplotlib.pyplot as plt
from utils import integrateForward, integrateBackward

def main(argv):
    def integrateForwardManually(deriv, t0, y0, dt, nTSteps):
        ts = np.empty(nTSteps)
        ys = np.empty(nTSteps)
        t = t0
        y = y0
        ts[0] = t
        ys[0] = y
        for i in range(1,nTSteps):
            t = t+dt
            y = y+dt*deriv(y=y, t=t)
            print("t=%.02f, value=%.02f"% (t, y))
            ts[i] = t
            ys[i] = y
        return {"times":ts, "ys":ys}

    def integrateBackwardManually(deriv, t0, y0, dt, nTSteps):
        ts = np.empty(nTSteps)
        ys = np.empty(nTSteps)
        t = t0
        y = y0
        ts[0] = t
        ys[0] = y
        for i in range(1,nTSteps):
            t = t-dt
            y = y-dt*deriv(y=y, t=t)
            print("t=%.02f, value=%.02f"% (t, y))
            ts[i] = t
            ys[i] = y
        return {"times":ts, "ys":ys}

    epsilon = 1e-6
    y0 = 1.0
    t0 = 0.0
    tf = 1.0
    dt = 1e-3
    # nTSteps = int(round((tf-t0)/dt))
    nTSteps = int(round((tf-t0)/dt))

    def deriv(y, t):
        return y

    # res = integrateForward(deriv=iNapIKModel.deriv, t0=t0, y0=y0, dt=dt, nTSteps=nTSteps)
    # res = integrateBackward(deriv=iNapIKModel.deriv, t0=tf, y0=y0, dt=dt, nTSteps=nTSteps)
    # res = integrateForwardManually(deriv=deriv, t0=t0, y0=y0*np.exp(t0), dt=dt, nTSteps=nTSteps)
    res = integrateBackwardManually(deriv=deriv, t0=tf, y0=y0*np.exp(tf), dt=dt, nTSteps=nTSteps)
    plt.plot(res["times"], res["ys"], label="numerical")
    plt.plot(res["times"], y0*np.exp(res["times"]), label="analytical")
    plt.legend()
    plt.xlabel("Time (sec)")
    plt.ylabel("Value")
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

