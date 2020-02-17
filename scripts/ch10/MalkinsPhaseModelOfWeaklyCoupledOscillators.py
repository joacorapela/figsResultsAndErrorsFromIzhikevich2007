
import numpy as np
import pdb

class MalkinsPhaseModelOfWeaklyCoupledOscillators:

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
            pi = self._getCouplingPulse(xsAtT=xsAtT, n=n, m=m, i=i, 
                                                     indicesI=indicesI)
            aDeriv[i] = aDeriv[i] + self._epsilon*self._qs[i](y[i])*pi
        return(aDeriv)

    def _getCouplingPulse(self, xsAtT, n, m, i, indicesI):
        pi = 0
        for j in xrange(n):
            indicesJ = j*m+np.arange(m)
            pi = pi + self._couplings[i][j](x1=xsAtT[indicesI], 
                                             x2=xsAtT[indicesJ])
        return(pi)
