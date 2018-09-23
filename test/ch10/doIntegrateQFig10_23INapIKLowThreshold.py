
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
    def normalizeQ(phase, Q, V, n): 
        QNormalization = Q.dot(iNapIKModel.deriv(t=phase, y=[V, n]))
        QNormalized = Q/QNormalization
        return QNormalized

    def integrateBackwardWithQNormalization(deriv, normalizeQ, phaseF, yf, 
                                                   dPhase, nPhases,
                                                   lcParamPhases, lcParamXs):
        phases = np.empty(nPhases)
        ys = np.empty((len(yf), nPhases))
        phase = phaseF
        y = yf
        phases[0] = phase
        ys[:,0] = y
        for i in range(1,nPhases):
            phase = phase-dPhase
            # find V and n
            integrationIndex = np.argmin(np.abs(phase-lcParamPhases))
            print("phase=%.4f, integrationPhase=%.4f"%
                  (phase, lcParamPhases[integrationIndex]))
            aux = lcParamXs[:,integrationIndex]
            V = aux[0]
            n = aux[1]
            #
            iNapIKDeriv = iNapIKModel.deriv(t=phase, y=(V,n))
            print("phase=%.02f, V=%.02f, n=%.02f, Q0=%.04f, Q1=%.04f"%
                  (phase, V, n, y[0], y[1]))
            print("f(gamma[phase])=(%.4f, %.4f), <Q,f(gamma[phase])>=%.4f"%
                  (iNapIKDeriv[0], iNapIKDeriv[1], y.dot(iNapIKDeriv)))
            y = normalizeQ(phase=phase, Q=y, V=V, n=n)
            y = y-dPhase*deriv(y=y, V=V, n=n)
            phases[i] = phase
            ys[:,i] = y
        # reversing phases and ys to be in increasing order of phases
        phases = phases[::-1]
        ys = ys[:,::-1]
        # done reversing
        return {"phases":phases, "ys":ys}

    def deriv(y, V, n):
        Q = y
        jacobianAtT = iNapIKModel.getJacobian(v0=V, n0=n)
        Qdot = -np.transpose(jacobianAtT).dot(Q)
        print("Qdot=[%.4f,%.4f]"%(Qdot[0],Qdot[1]))
        return Qdot

    i0 = 35.0
    Qf0 = -.04705
    Qf1 = None
    paramLimitCycleFilename = "results/paramLimitCyclesINapIKLowThresholdI0%.02f.npz"%(i0)
    resultsFilename = "results/integrationQINapIKLowThresholdI0%.02f.npz"%(i0)
    dPhase = 1e-3
    def i(t):
        return(i0)

    paramLimitCycleLoadRes = np.load(paramLimitCycleFilename)
    lcParamXs = paramLimitCycleLoadRes["limitCycle"]
    lcParamPhases = paramLimitCycleLoadRes["phases"]
    T = lcParamPhases[-1]
    phase0 = 0.0
    phaseF = T
    nPhases = int(round((phaseF-phase0)/dPhase))
    integrationIndex = np.argmin(np.abs(phaseF-lcParamPhases))
    print("phase=%.4f, integrationPhase=%.4f"%(phaseF, lcParamPhases[integrationIndex]))
    aux = lcParamXs[:,integrationIndex]
    vf = aux[0]
    nf = aux[1]
    # Lets find Q[0] such that <Q[0],f(gamma[0])>=1
    iNapIKModel = INapIKModel.getLowThresholdInstance()
    iNapIKModel.setI(i=i)
    ff = iNapIKModel.deriv(t=phaseF, y=[vf, nf])
    if Qf0 is None:
        Qf = np.array([(1.0-Qf1*ff[1])/ff[0], Qf1])
    else:
        Qf = np.array([Qf0, (1.0-Qf0*ff[0])/ff[1]])

    yf = np.array([Qf[0], Qf[1]])
    print("phase=%.02f, V=%.02f, n=%.02f, Q0=%.04f, Q1=%.04f"%
          (phaseF, vf, nf, yf[0], yf[1]))
    print("f(gamma[phase])=(%.4f, %.4f), <Q,f(gamma[phase])>=%.4f"%(ff[0], ff[1], yf.dot(ff)))

    qIntRes = integrateBackwardWithQNormalization(deriv=deriv,
                                                   normalizeQ=normalizeQ,
                                                   phaseF=phaseF, yf=yf,
                                                   dPhase=dPhase,
                                                   nPhases=nPhases,
                                                   lcParamPhases=lcParamPhases,
                                                   lcParamXs=lcParamXs)
    np.savez(resultsFilename, phases=qIntRes["phases"], ys=qIntRes["ys"])

    plt.plot(qIntRes["phases"], qIntRes["ys"][0,:], label="Q0", color="blue")
    plt.plot(qIntRes["phases"], 0.01*qIntRes["ys"][1,:], label="0.01 Q1", color="red")
    plt.xlabel("Phase (sec)")
    plt.ylabel("Q")
    plt.legend(loc="upper left")

    plt.figure()
    plt.plot(qIntRes["ys"][0,:], qIntRes["ys"][1,:], color="blue")
    plt.xlabel("Q0")
    plt.ylabel("Q1")

    plt.show()

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

