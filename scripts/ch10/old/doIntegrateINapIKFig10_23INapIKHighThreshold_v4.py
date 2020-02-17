
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
    def normalizeQ(t, Q, V, n, epsilon): 
        QNormalization = Q.dot(iNapIKModel.deriv(t=t, y=[V, n]))
        QNormalized = Q/QNormalization
        return QNormalized

    def integrateBackwardWithQNormalization(deriv, normalizeQ, tf, yf, dt, 
                                                   nTSteps):
        ts = np.empty(nTSteps)
        ys = np.empty((len(yf), nTSteps))
        t = tf
        y = yf
        ts[0] = t
        ys[:,0] = y
        for i in range(1,nTSteps):
            t = t-dt
            # find V and n
            integrationIndex = np.argmin(np.abs(t-iNapIKIntRes["times"]))
            print("t=%.4f, integrationT=%.4f"%(t, iNapIKIntRes["times"][integrationIndex]))
            aux = iNapIKIntRes["ys"][:,integrationIndex]
            V = aux[0]
            n = aux[1]
            #
            iNapIKDeriv = iNapIKModel.deriv(t=t, y=(V,n))
            print("t=%.02f, V=%.02f, n=%.02f, Q0=%.02f, Q1=%.02f"%
                  (t, V, n, y[0], y[1]))
            print("f(x[t])=(%.4f, %.4f), <Q,f(x[t])>=%.4f"%
                  (iNapIKDeriv[0], iNapIKDeriv[1], y.dot(iNapIKDeriv)))
            y = normalizeQ(t=t, Q=y, V=V, n=n, epsilon=epsilon)
            y = y-dt*deriv(y=y, t=t, V=V, n=n)
            ts[i] = t
            ys[:,i] = y
        return {"times":ts, "ys":ys}

    def deriv(y, t, V, n):
        Q = y
        jacobianAtT = iNapIKModel.getJacobian(v0=V, n0=n)
        Qdot = -np.transpose(jacobianAtT).dot(Q)
        print("Qdot=[%.4f,%.4f]"%(Qdot[0],Qdot[1]))
        return Qdot

    integrationINapIKFilename = 'results/integrationINapIKFig10_1.npz'
    resultsFilename = 'results/integrationQINapIKHighThresholdFig10_23.npz'
    epsilon = 1e-6
    t0 = 15.48299
    tf = 22.5565
    dt = 1e-3
    nTSteps = int(round((tf-t0)/dt))
    i0 = 10
    def i(t):
        return(i0)

    iNapIKIntRes = np.load(integrationINapIKFilename)
    integrationIndex = np.argmin(np.abs(tf-iNapIKIntRes["times"]))
    print("t=%.4f, integrationT=%.4f"%(tf, iNapIKIntRes["times"][integrationIndex]))
    aux = iNapIKIntRes["ys"][:,integrationIndex]
    vf = aux[0]
    nf = aux[1]
    # Lets find Q[0] such that <Q[0],f(x[0])>=1
    iNapIKModel = INapIKModel.getHighThresholdInstance()
    iNapIKModel.setI(i=i)
    ff = iNapIKModel.deriv(t=tf, y=[vf, nf])
    if abs(ff[1])>abs(ff[0]):
        Qf = np.array([0.0, 1/ff[1]])
    else:
        Qf = np.array([1/ff[0], 0.0])
    #

    yf = np.array([Qf[0], Qf[1]])
    print("t=%.02f, V=%.02f, n=%.02f, Q0=%.02f, Q1=%.02f"%
          (tf, vf, nf, yf[0], yf[1]))
    print("f(x[t])=(%.4f, %.4f), <Q,f(x[t])>=%.4f"%(ff[0], ff[1], yf.dot(ff)))

    qIntRes = integrateBackwardWithQNormalization(deriv=deriv, normalizeQ=normalizeQ, tf=tf, yf=yf, dt=dt, nTSteps=nTSteps)
    qIntRes["times"] = qIntRes["times"] - qIntRes["times"][-1] 
    np.savez(resultsFilename, times=qIntRes["times"], ys=qIntRes["ys"])

    plt.plot(qIntRes["times"], qIntRes["ys"][0,:], label="Q1", color="blue")
    plt.plot(qIntRes["times"], 0.01*qIntRes["ys"][1,:], label="0.01 Q2", color="red")
    plt.ylim((-0.5, 0.3))
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
    plt.xlim((-0.1, 0.3))
    plt.ylim((-50.0, 5.0))

    plt.show()

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

