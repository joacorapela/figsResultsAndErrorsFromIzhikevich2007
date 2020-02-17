
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
    resultsFilename = 'results/integrationQINapIKHighThresholdFig10_23.npz'
    epsilon = 1e-6
    v0 = -61.0
    n0 = 0.48
    t0 = 0.0
    tf = 1*7.25
    dt = 1e-3
    nTSteps = int(round((tf-t0)/dt))
    i0 = 10
    def i(t):
        return(i0)
    iNapIKModel = INapIKModel.getHighThresholdInstance()
    iNapIKModel.setI(i=i)
    # n0 = iNapIKModel._nInf(v=v0)

    # Lets find Q[0] such that <Q[0],f(x[0])>=1
    f0 = iNapIKModel.deriv(t=t0, y=[v0, n0])
    if abs(f0[1])>abs(f0[0]):
        Q0 = np.array([0.0, 1/f0[1]])
    else:
        Q0 = np.array([1/f0[0], 0.0])

    # scaleMatrix = 1e-0*np.array([[1.0,0.0],[0.0,1e-2]])
    scaleMatrix = np.array([[1.0,0.0],[0.0,0.1]])
    Q0 = scaleMatrix.dot(Q0)
    y0 = np.array([v0, n0, Q0[0], Q0[1]])

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
            y[2:] = QNormalized
            ts[i] = t
            ys[:,i] = y
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
            print("t=%.02f, V=%.02f, n=%.02f, Q0=%.02f, Q1=%.02f"%
                  (t, y[0], y[1], y[2], y[3]))
            QNormalized = normalizeQ(t=t, Q=y[2:], V=y[0], n=y[1])
            y[2:] = QNormalized
            ts[i] = t
            ys[:,i] = y
        return {"times":ts, "ys":ys}

    def deriv(y, t):
        V = y[0]
        n = y[1]
        Q = y[2:]
        iNapIKModelDeriv = iNapIKModel.deriv(t=t, y=[V,n])
        # print("t=%f, V=%.4f, n=%.4f, Q=[%.4f,%.4f]"%(t, V, n, Q[0],Q[1]))
        print("<Q,f(x[t])>=%.4f"%(Q.dot(iNapIKModelDeriv)))
        jacobianAtT = iNapIKModel.getJacobian(v0=V, n0=n)
        Qdot = -scaleMatrix.dot(np.transpose(jacobianAtT)).dot(Q)
        print("Vdot=%.4f, nDot=%.4f, Qdot=[%.4f,%.4f]"%(iNapIKModelDeriv[0],
                                                         iNapIKModelDeriv[1],
                                                         Qdot[0],Qdot[1]))
        deriv = np.concatenate([iNapIKModelDeriv, Qdot])
        # pdb.set_trace()
        return deriv

#     qIntRes = integrateForward(deriv=deriv, t0=t0, y0=y0, dt=dt, nTSteps=nTSteps)
#     qIntRes = integrateBackward(deriv=deriv, t0=tf, y0=y0, dt=dt, nTSteps=nTSteps)
#     qIntRes = integrateForwardWithQNormalization(deriv=deriv, normalizeQ=normalizeQ, t0=t0, y0=y0, dt=dt, nTSteps=nTSteps)
    qIntRes = integrateBackwardWithQNormalization(deriv=deriv, normalizeQ=normalizeQ, t0=tf, y0=y0, dt=dt, nTSteps=nTSteps)
    np.savez(resultsFilename, times=qIntRes["times"], ys=qIntRes["ys"])

    plt.plot(qIntRes["times"], qIntRes["ys"][2,:], label="Q1", color="blue")
    plt.plot(qIntRes["times"], qIntRes["ys"][3,:], label="Q2", color="red")
    # plt.ylim([-1,1])
    plt.xlabel("Time (sec)")
    plt.ylabel("Q")
    plt.legend(loc="lower right")
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(qIntRes["times"], qIntRes["ys"][0,:], label="V", color="gray")
    ax2.legend(loc="lower left")
    ax2.set_ylabel("Membrane\nPotential (mV)")

    plt.figure()
    plt.plot(qIntRes["ys"][2,:], qIntRes["ys"][3,:], color="blue")
    plt.xlabel("Q1")
    plt.ylabel("Q2")

    plt.show()

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

