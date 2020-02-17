
import sys
import numpy as np
import pdb
# from scipy.integrate import ode
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateForward
from utils import integrateBackward

def main(argv):
    integrationINapIKFilename = 'results/integrationINapIKFig10_1.npz'
    resultsFilename = 'results/integrationQINapIKHighThresholdFig10_23.npz'
    epsilon = 1e-6
    v0 = -60.00
    n0 = 0.001
    t0 = 0.0
    tf = 1*7.25
    dt = 1e-3
    nTSteps = int(round((tf-t0)/dt))
    i0 = 10
    def i(t):
        return(i0)

    # Lets find Q[0] such that <Q[0],f(x[0])>=1
    iNapIKModel = INapIKModel.getHighThresholdInstance()
    iNapIKModel.setI(i=i)
    f0 = iNapIKModel.deriv(t=t0, y=[v0, n0])
    if abs(f0[1])>abs(f0[0]):
        Q0 = np.array([0.0, 1/f0[1]])
    else:
        Q0 = np.array([1/f0[0], 0.0])

    iNapIKIntRes = np.load(integrationINapIKFilename)

    # scaleMatrix = 1e-0*np.array([[1.0,0.0],[0.0,1e-2]])
    scaleMatrix = np.array([[1.0,0.0],[0.0,0.1]])
    Q0 = scaleMatrix.dot(Q0)
    y0 = np.array([Q0[0], Q0[1]])

    def normalizeQ(t, Q, V, n): 
        QNormalization = Q.dot(iNapIKModel.deriv(t=t, y=[V, n]))
        QNormalized = Q/QNormalization
        return QNormalized

    def integrateForwardWithQNormalization(deriv, normalizeQ, t0, y0, dt, 
                                                  nTSteps):
        ts = np.empty(nTSteps)
        ys = np.empty((len(y0), nTSteps))
        t = t0
        y = y0
        ts[0] = t
        ys[:,0] = y
        for i in range(1,nTSteps):
            t = t+dt
            y = y+dt*deriv(y=y, t=t)
            print("t=%.02f, V=%.02f, n=%.02f, Q0=%.02f, Q1=%.02f"%
                  (t, y[0], y[1], y[2], y[3]))
            QNormalized = normalizeQ(t=t, Q=y[2:], V=y[0], n=y[1])
            ts[i] = t
            ys[:,i] = QNormalized
        return {"times":ts, "ys":ys}

    def integrateBackwardWithQNormalization(deriv, normalizeQ, t0, y0, dt, 
                                                   nTSteps):
        ts = np.empty(nTSteps)
        ys = np.empty((len(y0), nTSteps))
        t = t0
        y = y0
        ts[0] = t
        ys[:,0] = y
        for i in range(1,nTSteps):
            t = t-dt
            y = y-dt*deriv(y=y, t=t)
            print("t=%.02f, Q0=%.02f, Q1=%.02f"%
                  (t, y[0], y[1]))
            # QNormalized = normalizeQ(t=t, Q=y[2:], V=y[0], n=y[1])
            ts[i] = t
            ys[:,i] = y
        return {"times":ts, "ys":ys}

    def deriv(y, t):
        Q = y
        integrationIndex = np.argmin(np.abs(t-iNapIKIntRes["times"]))
        print("t=%.4f, integrationT=%.4f"%(t, iNapIKIntRes["times"][integrationIndex]))
        print("Q=[%.4f,%.4f]"%(Q[0],Q[1]))
        yt = iNapIKIntRes["ys"][:,integrationIndex]
        print("<Q,f(x[t])>=%.4f"%(Q.dot(iNapIKModel.deriv(t=t, y=yt))))
        jacobianAtT = iNapIKModel.getJacobian(v0=yt[0], n0=yt[1])
        Qdot = -scaleMatrix.dot(np.transpose(jacobianAtT)).dot(Q)
        print("Qdot=[%.4f,%.4f]"%(Qdot[0],Qdot[1]))
        # pdb.set_trace()
        return Qdot

#     qIntRes = integrateForward(deriv=deriv, t0=t0, y0=y0, dt=dt, nTSteps=nTSteps)
#     qIntRes = integrateBackward(deriv=deriv, t0=tf, y0=y0, dt=dt, nTSteps=nTSteps)
#     qIntRes = integrateForwardWithQNormalization(deriv=deriv, normalizeQ=normalizeQ, t0=t0, y0=y0, dt=dt, nTSteps=nTSteps)
    qIntRes = integrateBackwardWithQNormalization(deriv=deriv, normalizeQ=normalizeQ, t0=tf, y0=y0, dt=dt, nTSteps=nTSteps)
#     qIntRes = integrateBackward(deriv=deriv, t0=tf, y0=Q0, dt=dt, nTSteps=nTSteps)
    np.savez(resultsFilename, times=qIntRes["times"], ys=qIntRes["ys"])

    plt.plot(qIntRes["times"], qIntRes["ys"][0,:], label="Q1", color="blue")
    plt.plot(qIntRes["times"], qIntRes["ys"][1,:], label="Q2", color="red")
    # plt.ylim([-1,1])
    plt.xlabel("Time (sec)")
    plt.ylabel("Q")
    plt.legend(loc="lower right")
#     ax = plt.gca()
#     ax2 = ax.twinx()
#     ax2.plot(qIntRes["times"], qIntRes["ys"][0,:], label="V", color="gray")
#     ax2.legend(loc="lower left")
#     ax2.set_ylabel("Membrane\nPotential (mV)")

    plt.figure()
    plt.plot(qIntRes["ys"][0,:], qIntRes["ys"][1,:], color="blue")
    plt.xlabel("Q1")
    plt.ylabel("Q2")

    plt.show()

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

