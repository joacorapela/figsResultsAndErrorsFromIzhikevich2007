
import numpy as np
import pdb
from utils import boltzmann, derBoltzmannWRTV, getStabilityType

class IKModel:

    def __init__(self, i, c=1.0, gL=1.0, eL=-80.0, gK=1.0, eK=-90.0, 
                       mVOneHalf=-53.0, mK=15.0, tau=lambda v: 1.0):

        self._i = i
        self._c = c
        self._gL = gL
        self._eL = eL
        self._gK = gK
        self._eK = eK
        self._mVOneHalf = mVOneHalf
        self._mK = mK
        self._tau = tau

    def deriv(self, t, y):
        v = y[0]
        m = y[1]

        vDot = (self._i(t)-self.getIInf(y=y))/self._c
        mDot = (self._mInf(v)-m)/self._tau(v)
        return(np.array([vDot, mDot]))

    def getIInf(self, y):
        v = y[0]
        m = y[1]
        i = self._gL*(v-self._eL) + \
             self._gK*pow(self._mInf(v=v),4)*(v-self._eK)
        return(i)

    def getFuncVDotAtMInf(self, i0):
        answer = lambda v: i0-self._gL*(v-self._eL)-\
                              self._gK*pow(self._mInf(v),4)*(v-self._eK)
        return(answer)

    def checkStability(self, i0, v0, m0, tauDeriv=lambda v: 0.0):
        f = self.getFuncVDotAtMInf(i0=i0)
        print('vDotAtV0=%.04f'%(f(v=v0)))

        a = -self._gL-self._gK*pow(m0, 4)
        b = -self._gK*4*pow(m0, 3)*(v0-self._eK)
        c = (self._derMInf(v=v0)*self._tau(v=v0)-
             (self._mInf(v=v0)-m0)*tauDeriv(v=v0))/self._tau(v=v0)**2
        d = -1.0/self._tau(v0)

        jacobian = np.array([[a, b], [c, d]])
        eigRes = np.linalg.eig(jacobian)
        stabilityType = getStabilityType(eigvals=eigRes[0])
        return(stabilityType, eigRes[0])

    def _mInf(self, v):
        return(boltzmann(v=v, vOneHalf=self._mVOneHalf, k=self._mK))

    def _derMInf(self, v):
        return(derBoltzmannWRTV(v=v, vOneHalf=self._mVOneHalf, k=self._mK))
