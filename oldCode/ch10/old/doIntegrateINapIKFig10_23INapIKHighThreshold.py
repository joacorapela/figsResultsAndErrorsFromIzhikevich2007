
import sys
import numpy as np
import pdb
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateForward

def main(argv):
    integrationINapIKFilename = 'results/integrationINapIKFig10_1.npz'
    resultsFilename = 'results/integrationQINapIKHighThresholdFig10_23.npz'
    epsilon = 1e-6
    v0 = -60.00
    n0 = 0.001
    t0 = 0.0
    tf = 10.0
    dt = 1e-5
    nTSteps = int(round((tf-t0)/dt))
    i0 = 10
    def i(t):
        return(i0)
    iNapIKModel = INapIKModel.getHighThresholdInstance()
    iNapIKModel.setI(i=i)
    # n0 = iNapIKModel._nInf(v=v0)
    y0 = np.array([v0, n0])

    # Lets find Q[0] such that <Q[0],f(x[0])>=1
    f0 = iNapIKModel.deriv(t=0.0, y=y0)
    if abs(f0[1])>abs(f0[0]):
        Q0 = np.array([0.0, 1/f0[1]])
    else:
        Q0 = np.array([1/f0[0], 0.0])

    iNapIKIntRes = np.load(integrationINapIKFilename)

    scaleMatrix = np.array([[1.0,0.0],[0.0,1e-2]])
    Q0 = scaleMatrix.dot(Q0)
    def deriv(t, Q):
        integrationIndex = np.argmin(np.abs(t-iNapIKIntRes["times"]))
        print("t=%.4f, integrationT=%.4f"%(t, iNapIKIntRes["times"][integrationIndex]))
        print("Q=[%.4f,%.4f]"%(Q[0],Q[1]))
        yt = iNapIKIntRes["ys"][:,integrationIndex]
        # QNormalization = Q.dot(iNapIKModel.deriv(t=t, y=yt))
        # Q = Q/QNormalization
        jacobianAtT = iNapIKModel.getJacobian(v0=yt[0], n0=yt[1])
        # Qdot = -np.transpose(jacobianAtT).dot(Q)
        Qdot = -np.transpose(jacobianAtT.dot(scaleMatrix)).dot(Q)
        print("Qdot=[%.4f,%.4f]"%(Qdot[0],Qdot[1]))
        print("<Q,f(x[t])>=%.4f"%(Q.dot(iNapIKModel.deriv(t=t, y=yt))))
        # pdb.set_trace()
        return Qdot

    qIntRes = integrateForward(deriv=deriv, y0=Q0, dt=dt, nTSteps=nTSteps)

    np.savez(resultsFilename, times=qIntRes['times'], 
                              ys=qIntRes['ys'])

    plt.plot(qIntRes["times"], qIntRes["ys"][0,:], label="Q1")
    plt.plot(qIntRes["times"], qIntRes["ys"][1,:], label="Q2")
    plt.ylim([-1,1])
    plt.xlabel("Time (sec)")
    plt.ylabel("Q")
    plt.legend()
    plt.show()

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

