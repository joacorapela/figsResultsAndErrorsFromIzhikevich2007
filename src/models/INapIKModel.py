
import numpy as np
import pdb
from utils.myMath import findZeroByBisection

class INapIKModel:

    def __init__(self, c, gL, eL, gNa, eNa, gK, eK, 
                       mVOneHalf, mK, nVOneHalf, nK, tau):
        self._c = c
        self._gL = gL
        self._eL = eL
        self._gNa = gNa
        self._eNa = eNa
        self._gK = gK
        self._eK = eK
        self._mVOneHalf = mVOneHalf
        self._mK = mK
        self._nVOneHalf = nVOneHalf
        self._nK = nK
        self._tau = tau

    def setI(self, i):
        self._i = i

    @classmethod
    def getLowThresholdInstance(cls, c=1.0, 
                                     gL=8.0, eL=-78.0, 
                                     gNa=20.0, eNa=60.0, 
                                     gK=10.0, eK=-90.0, 
                                     mVOneHalf=-20.0, mK=15.0, 
                                     nVOneHalf=-45.0, nK=5.0, 
                                     tau=lambda v: 1.0):
        return(cls(c=c, gL=gL, eL=eL, gNa=gNa, eNa=eNa, gK=gK, eK=eK, 
                        mVOneHalf=mVOneHalf, mK=mK, nVOneHalf=nVOneHalf, 
                        nK=nK, tau=tau))

    @classmethod
    def getHighThresholdInstance(cls, c=1.0, 
                                      gL=8.0, eL=-80.0, 
                                      gNa=20.0, eNa=60.0,
                                      gK=10.0, eK=-90.0, 
                                      mVOneHalf=-20.0, mK=15.0, 
                                      nVOneHalf=-25.0, nK=5.0, 
                                      tau=lambda v: 1.0):
        return(cls(c=c, gL=gL, eL=eL, gNa=gNa, eNa=eNa, gK=gK, eK=eK, 
                        mVOneHalf=mVOneHalf, mK=mK, nVOneHalf=nVOneHalf, 
                        nK=nK, tau=tau))

    def deriv(self, y, t):
        v = y[0]
        n = y[1]

        vDot = (self._i(t)-self.getChannelsI(y=y))/self._c
        nDot = (self._nInf(v)-n)/self._tau(v)
        return(np.array([vDot, nDot]))

    def getChannelsI(self, y):
        v = y[0]
        n = y[1]
        i = self._gL*(v-self._eL) + \
             self._gNa*self._mInf(v=v)*(v-self._eNa) + \
             self._gK*n*(v-self._eK)
        return(i)

    def getIInf(self, v):
        y = (v, self._nInf(v=v))
        return(self.getChannelsI(y=y))

    def getFuncVDotAtNInf(self, i0):
        answer = lambda v: (i0-self._gL*(v-self._eL)-self._gNa*self._mInf(v)*(v-self._eNa)-self._gK*self._nInf(v)*(v-self._eK))/self._c
        return(answer)

    def getJacobian(self, v0, n0, tauDeriv=lambda v: 0.0):
        mInfV0 = self._mInf(v0)
        nInfV0 = self._nInf(v0)
        dMInfV0 = 1.0/self._mK*mInfV0*(1-mInfV0)
        dNInfV0 = 1.0/self._nK*nInfV0*(1-nInfV0)

        a = (-self._gL-\
              self._gNa*(dMInfV0*(v0-self._eNa)+mInfV0)-\
              self._gK*n0)/self._c
        b = -self._gK*(v0-self._eK)/self._c
        c = (dNInfV0*self._tau(v0)-(nInfV0-n0)*tauDeriv(v0))/self._tau(v0)**2
        d = -1.0/self._tau(v0)

        jacobian = np.array([[a, b], [c, d]])
        return jacobian

    def checkStability(self, v0, n0, tauDeriv=lambda v: 0.0):
        jacobian = self.getJacobian(v0=v0, n0=n0, tauDeriv=tauDeriv)
        eigRes = np.linalg.eig(jacobian)
        stabilityType = getStabilityType(eigvals=eigRes[0])
        return(stabilityType, eigRes[0], jacobian)

    def getIntersectionOfNullclines(self, vMin=-50, vMax=-20, tol=1e-6):
        def functionToFindZero(v):
            return self._gL*(v-self._eL)+\
                   self._gNa*self._mInf(v=v)*(v-self._eNa)+\
                   self._gK*self._nInf(v=v)*(v-self._eK)-\
                   self._i(t=0)
        v = findZeroByBisection(f=functionToFindZero, xMin=vMin, xMax=vMax, 
                                                      tol=tol)
        n = self._nInf(v=v)
        return(np.array([v, n]))

    def _mInf(self, v):
        return(self._boltzmann(v=v, vOneHalf=self._mVOneHalf, k=self._mK))

    def _nInf(self, v):
        return(self._boltzmann(v=v, vOneHalf=self._nVOneHalf, k=self._nK))

    def _boltzmann(self, v, vOneHalf, k):
        return(1.0/(1.0+np.exp((vOneHalf-v)/k)))


