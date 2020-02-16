
import numpy as np
import pdb

class ApproxHodgkinAndHuxleyModel:
    STABLE = 0
    UNSTABLE = 1
    def __init__(self, i, c=1, gL=0.3, eL=10.6, gNaMax=120.0, eNa=120.0, 
                       gKMax=36.0, eK=-12.0, 
                       nVOneHalf=11.59, nK=14.86, 
                       mVOneHalf=24.97, mK=9.14,
                       hVOneHalf=2.69, hK=-7.07,
# The following are the parameters I computed
                       nCBase=1.07, nCAmp=4.72, nVMax=-12.17, nSigma=47.61,
                       mCBase=0.13, mCAmp=0.37, mVMax=26.16, mSigma=33.50,
                       hCBase=1.00, hCAmp=7.58, hVMax=-1.81, hSigma=20.04):
# The following are the parameters from Izhikevich's book
#                        nCBase=1.1, nCAmp=4.7, nVMax=-14.0, nSigma=50.0,
#                        mCBase=0.04, mCAmp=0.46, mVMax=27.0, mSigma=30.0,
#                        hCBase=1.2, hCAmp=7.4, hVMax=-2.0, hSigma=20.0):
        self._i = i
        self._c = c
        self._gL = gL
        self._eL = eL
        self._gNaMax = gNaMax
        self._eNa = eNa
        self._gKMax = gKMax
        self._eK = eK
        self._nVOneHalf=nVOneHalf
        self._nK=nK
        self._mVOneHalf=mVOneHalf,
        self._mK=mK
        self._hVOneHalf=hVOneHalf
        self._hK=hK
        self._nCBase = nCBase
        self._nCAmp = nCAmp
        self._nVMax = nVMax
        self._nSigma = nSigma
        self._mCBase = mCBase
        self._mCAmp = mCAmp
        self._mVMax = mVMax
        self._mSigma = mSigma
        self._hCBase = hCBase
        self._hCAmp = hCAmp
        self._hVMax = hVMax
        self._hSigma = hSigma

    def deriv(self, t, y):
        v = y[0]
        n = y[1]
        m = y[2]
        h = y[3]

        vDot = (self._i(t)-self.getIInf(y=y))/self._c
        nDot = (self._nInf(v=v)-n)/self._tauN(v=v)
        mDot = (self._mInf(v=v)-m)/self._tauM(v=v)
        hDot = (self._hInf(v=v)-h)/self._tauH(v=v)
        return(np.array([vDot, nDot, mDot, hDot]))

    def getIInf(self, y):
        v = y[0]
        n = y[1]
        m = y[2]
        h = y[3]
        i = self._gL*(v-self._eL) + \
             self._gNaMax*pow(m, 3)*h*(v-self._eNa) + \
             self._gKMax*pow(n,4)*(v-self._eK)
        return(i)

    def _nInf(self, v):
        return(1.0/(1+np.exp((self._nVOneHalf-v)/self._nK)))

    def _derNInf(self, v):
        nInf = self._nInf(v=v)
        return(nInf/self._nK*(1-nInf))

    def _tauN(self, v):
        return(self._nCBase+\
                self._nCAmp*np.exp(-(self._nVMax-v)**2/self._nSigma**2))

    def _mInf(self, v):
        return(1.0/(1+np.exp((self._mVOneHalf-v)/self._mK)))

    def _derMInf(self, v):
        mInf = self._mInf(v=v)
        return(mInf/self._mK*(1-mInf))

    def _tauM(self, v):
        return(self._mCBase+\
                self._mCAmp*np.exp(-(self._mVMax-v)**2/self._mSigma**2))

    def _hInf(self, v):
        return(1.0/(1+np.exp((self._hVOneHalf-v)/self._hK)))

    def _derHInf(self, v):
        hInf = self._hInf(v=v)
        return(hInf/self._hK*(1-hInf))

    def _tauH(self, v):
        return(self._hCBase+\
                self._hCAmp*np.exp(-(self._hVMax-v)**2/self._hSigma**2))

    def checkStability(self, v):
        derFV = -self._gL-\
                 self._gKMax*(4*pow(self._nInf(v=v),3)*self._derNInf(v=v)*\
                              (v-self._eK)+pow(self._nInf(v=v),4))-\
                 self._gNaMax*(3*pow(self._mInf(v=v),2)*self._derMInf(v=v)*\
                               self._hInf(v=v)*(v-self._eNa)+\
                               pow(self._mInf(v=v),3)*self._derHInf(v=v)*\
                               (v-self._eNa)+\
                               pow(self._mInf(v=v),3)*self._hInf(v=v))
        if derFV<=0:
            return(self.STABLE)
        return(self.UNSTABLE)
