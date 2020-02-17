
import sys
import numpy as np
import pdb
# from scipy.integrate import ode
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateBackward
from utils import computeLimitCycleAmplitudeAndPeriod

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
            integrationIndex = np.argmin(np.abs(t-iNapIKIntRes["times%dUncoupled"%(oscillatorIndex)]))
            print("t=%.4f, integrationT=%.4f"%(t, iNapIKIntRes["times%dUncoupled"%(oscillatorIndex)][integrationIndex]))
            aux = iNapIKIntRes["ys%dUncoupled"%(oscillatorIndex)][:,integrationIndex]
            V = aux[0]
            n = aux[1]
            #
            iNapIKDeriv = iNapIKModel.deriv(t=t, y=(V,n))
            print("t=%.02f, V=%.02f, n=%.02f, Q0=%.04f, Q1=%.04f"%
                  (t, V, n, y[0], y[1]))
            print("f(x[t])=(%.4f, %.4f), <Q,f(x[t])>=%.4f"%
                  (iNapIKDeriv[0], iNapIKDeriv[1], y.dot(iNapIKDeriv)))
            y = normalizeQ(t=t, Q=y, V=V, n=n, epsilon=epsilon)
            y = y-dt*deriv(y=y, t=t, V=V, n=n)
            ts[i] = t
            ys[:,i] = y
        ts = ts[::-1]
        ys = ys[:,::-1]
        return {"times":ts, "ys":ys}

    def deriv(y, t, V, n):
        Q = y
        jacobianAtT = iNapIKModel.getJacobian(v0=V, n0=n)
        Qdot = -np.transpose(jacobianAtT).dot(Q)
        print("Qdot=[%.4f,%.4f]"%(Qdot[0],Qdot[1]))
        return Qdot

    epsilon = 0.003
    i0 = 35.0
    couplingStartTime = 100.44
    # oscillatorIndex = 0
    # Qf0 = -.0475
    # Qf1 = None
    oscillatorIndex = 1
    Qf0 = None
    Qf1 = 85.85
    integrationINapIKFilename = "results/integrationWCoupledINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    resultsFilename = "results/integrationQINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f_oscillator%d.npz"%(i0, epsilon, couplingStartTime, oscillatorIndex)
    dt = 1e-3
    def i(t):
        return(i0)

    iNapIKIntRes = np.load(integrationINapIKFilename)
    xs = iNapIKIntRes["ys%dUncoupled"%(oscillatorIndex)]
    times = iNapIKIntRes["times%dUncoupled"%(oscillatorIndex)]
    T = computeLimitCycleAmplitudeAndPeriod(xs=xs[0,:], times=times)["period"]
    t0 = couplingStartTime
    tf = t0+T
    nTSteps = int(round((tf-t0)/dt))
    integrationIndex = np.argmin(np.abs(tf-iNapIKIntRes["times%dUncoupled"%(oscillatorIndex)]))
    print("t=%.4f, integrationT=%.4f"%(tf, iNapIKIntRes["times%dUncoupled"%(oscillatorIndex)][integrationIndex]))
    aux = iNapIKIntRes["ys%dUncoupled"%(oscillatorIndex)][:,integrationIndex]
    vf = aux[0]
    nf = aux[1]
    # Lets find Q[0] such that <Q[0],f(x[0])>=1
    iNapIKModel = INapIKModel.getLowThresholdInstance()
    iNapIKModel.setI(i=i)
    ff = iNapIKModel.deriv(t=tf, y=[vf, nf])
    if Qf0 is None:
        Qf = np.array([(1.0-Qf1*ff[1])/ff[0], Qf1])
    else:
        Qf = np.array([Qf0, (1.0-Qf0*ff[0])/ff[1]])

    yf = np.array([Qf[0], Qf[1]])
    print("t=%.02f, V=%.02f, n=%.02f, Q0=%.04f, Q1=%.04f"%
          (tf, vf, nf, yf[0], yf[1]))
    print("f(x[t])=(%.4f, %.4f), <Q,f(x[t])>=%.4f"%(ff[0], ff[1], yf.dot(ff)))

    qIntRes = integrateBackwardWithQNormalization(deriv=deriv, normalizeQ=normalizeQ, tf=tf, yf=yf, dt=dt, nTSteps=nTSteps)
    qIntRes["times"] = qIntRes["times"] - qIntRes["times"][0] 
    np.savez(resultsFilename, times=qIntRes["times"], ys=qIntRes["ys"])

    plt.plot(qIntRes["times"], qIntRes["ys"][0,:], label="Q0", color="blue")
    plt.plot(qIntRes["times"], 0.01*qIntRes["ys"][1,:], label="0.01 Q1", color="red")
#     plt.ylim((-0.5, 0.3))
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
    plt.xlabel("Q0")
    plt.ylabel("Q1")
#     plt.xlim((-0.1, 0.3))
#     plt.ylim((-50.0, 5.0))

    plt.show()

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

