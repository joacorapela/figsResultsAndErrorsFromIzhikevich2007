
import numpy as np
import pdb

class INatModel:

    STABLE_NODE = 0
    UNSTABLE_NODE = 1
    STABLE_FOCUS = 2
    UNSTABLE_FOCUS = 3
    SADDLE = 4

    def __init__(self, i, c, gL, eL, gNa, eNa, 
                       mVOneHalf, mK, hVOneHalf, hK, 
                       tauH=lambda v: 5.0):
        self._i = i
        self._c = c
        self._gL = gL
        self._eL = eL
        self._gNa = gNa
        self._eNa = eNa
        self._mVOneHalf = mVOneHalf
        self._mK = mK
        self._hVOneHalf = hVOneHalf
        self._hK = hK
        self._tauH = tauH

    @classmethod
    def getHighThresholdInstance(cls, i, c=1.0, 
                                     gL=1.0, eL=-70.0, 
                                     gNa=10.0, eNa=60.0, 
                                     mVOneHalf=-40.0, mK=15.0,
                                     hVOneHalf=-42.0, hK=-7.0,
                                     tauH=lambda v: 5.0):
        return(cls(i=i, c=c, gL=gL, eL=eL, gNa=gNa, eNa=eNa,
                        mVOneHalf=mVOneHalf, mK=mK, 
                        hVOneHalf=hVOneHalf, hK=hK, tauH=tauH))

    @classmethod
    def getLowThresholdInstance(cls, i, c=1.0, 
                                     gL=1.0, eL=-70.0, 
                                     gNa=15.0, eNa=60.0,
                                     mVOneHalf=-40.0, mK=15.0,
                                     hVOneHalf=-62.0, hK=-7.0,
                                     tauH=lambda v: 5.0):
        return(cls(i=i, c=c, gL=gL, eL=eL, gNa=gNa, eNa=eNa,
                        mVOneHalf=mVOneHalf, mK=mK, 
                        hVOneHalf=hVOneHalf, hK=hK, tauH=tauH))

    def deriv(self, t, y):
        v = y[0]
        h = y[1]

        vDot = (self._i(t)-self.getIInf(y=y))/self._c
        hDot = (self._hInf(v)-h)/self._tauH(v)
        return(np.array([vDot, hDot]))

    def getIInf(self, y):
        v = y[0]
        h = y[1]
        i = self._gL*(v-self._eL) + \
             self._gNa*pow(self._mInf(v), 3)*h*(v-self._eNa)
        return(i)

    def getFuncVDotAtHInf(self, i0):
        answer = lambda v: (i0-self._gL*(v-self._eL)-\
                               self._gNa*pow(self._mInf(v),3)* self._hInf(v)*\
                               (v-self._eNa))/self._c
        return(answer)

    def checkStability(self, i0, v0, h0, tauDeriv=lambda v: 0.0):
        f = self.getFuncVDotAtHInf(i0=i0)
        print('vDotAtV0=%.04f'%(f(v=v0)))

        mInfV0 = self._mInf(v0)
        hInfV0 = self._hInf(v0)

        a = (-self._gL-\
              self._gNa*h0*pow(mInfV0,3)*\
              (3.0/self._mK*(1-mInfV0)*(v0-self._eNa)+1))/self._c
        b = -self._gNa*pow(mInfV0,3)*(v0-self._eNa)/self._c
        c = ((hInfV0-hInfV0**2)/self._hK*self._tauH(v0)-\
             (hInfV0-h0)*tauDeriv(v0))/self._tauH(v0)**2
        d = -1.0/self._tauH(v0)

        jacobian = np.array([[a, b], [c, d]])
        eigRes = np.linalg.eig(jacobian)
        stabilityType = self._getStabilityType(eigvals=eigRes[0])
        return(stabilityType, eigRes[0])

    def _getStabilityType(self, eigvals, smallValue=1e-4):
        if isinstance(eigvals[0], complex) and abs(eigvals[0])>smallValue and\
           isinstance(eigvals[1], complex) and abs(eigvals[1])>smallValue:
            if eigvals[0].real>=0 and eigvals[1].real>=0:
                return(self.UNSTABLE_FOCUS)
            elif eigvals[0].real<0 and eigvals[1].real<0:
                return(self.STABLE_FOCUS)
            else:
                raise ValueError("Invalid eigvals ", eigvals)
        elif eigvals[0]>=0 and eigvals[1]>=0:
            return(self.UNSTABLE_NODE)
        elif eigvals[0]<0 and eigvals[1]<0:
            return(self.STABLE_NODE)
        elif (eigvals[0]<0 and eigvals[1]>=0) or \
             (eigvals[0]>=0 and eigvals[1]<0):
            return(self.SADDLE)
        else:
            raise ValueError("Invalid eigvals ", eigvals)

    def _mInf(self, v):
        return(self._boltzmann(v=v, vOneHalf=self._mVOneHalf, k=self._mK))

    def _hInf(self, v):
        return(self._boltzmann(v=v, vOneHalf=self._hVOneHalf, k=self._hK))

    def _boltzmann(self, v, vOneHalf, k):
        return(1.0/(1.0+np.exp((vOneHalf-v)/k)))

