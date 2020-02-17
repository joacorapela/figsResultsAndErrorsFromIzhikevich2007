
import numpy as np
import pdb

class MalkinsPhaseDeviationModelOfWeaklyCoupledOscillators:

    # couplings should be a list of lists of lists
    # couplings[k][i][j](xi, xj) is the coupling for the state variable k
    # to oscillator i from oscillator j
    def __init__(self, xs, xsTimes, qs, couplings, epsilon, couplingStartTime):
        self._xs = xs
        self._xsTimes = xsTimes
        self._qs = qs
        self._couplings = couplings
        self._epsilon = epsilon
        self._couplingStartTime = couplingStartTime

    def deriv(self, y, t):
        xsTimeIndex = np.argmin(np.abs(self._xsTimes-t))
        xsAtT = self._xs[:,xsTimeIndex]
        n = len(y)
        m = len(self._xs)/n
        aDeriv = np.ones(n)
        if t<=self._couplingStartTime:
            return aDeriv
        for i in xrange(n):
            indicesI = i*m+np.arange(m)
            aSumi = 0;
            for k in xrange(m):
                pik = self._getCouplingPulse(xsAtT=xsAtT, n=n, m=m, 
                                                          i=i, k=k,
                                                          indicesI=indicesI)
                print("Coupling pulse(i=%d, k=%d, t=%.04f)=%.04f"%(i, k, t, pik))
                qkThetai = self._qs[k](y[i])
                print("Q%d(unwrapped theta%d=%.04f)=%.04f"%(k, i, y[i],
                                                               qkThetai))
                aSumi = aSumi + qkThetai*pik
                print("sum(%d)=%.4f"%(i, aSumi))
            phaseDeviationi = self._epsilon*aSumi
            print("Phase deviation%d(t=%.04f)=%.04f"%(i, t, phaseDeviationi))
            aDeriv[i] = aDeriv[i] + phaseDeviationi
            print("deriv%d(t=%.04f)=%.04f"%(i, t, aDeriv[i]))
            print("----------")
        print("deriv(t=%.04f)=(%.04f,%.04f)"%(t, aDeriv[0], aDeriv[1]))
        print("********************************************************************************")
        return(aDeriv)

    # Answer coupling pulse for state variable k of oscillator i
    def _getCouplingPulse(self, xsAtT, n, m, i, k, indicesI):
        pik = 0
        for j in xrange(n):
            indicesJ = j*m+np.arange(m)
            pik = pik + self._couplings[k][i][j](x1=xsAtT[indicesI], 
                                                  x2=xsAtT[indicesJ])
        return(pik)
