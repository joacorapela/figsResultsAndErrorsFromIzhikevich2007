
import numpy as np
import pdb

class HodgkinAndHuxleyModel:

    def __init__(self, i, c=1, gL=0.3, eL=10.6, gNaMax=120.0, eNa=120.0, 
                       gKMax=36.0, eK=-12.0):
        self._i = i
        self._c = c
        self._gL = gL
        self._eL = eL
        self._gNaMax = gNaMax
        self._eNa = eNa
        self._gKMax = gKMax
        self._eK = eK

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
        return(self._alphaN(v)/(self._alphaN(v)+self._betaN(v)))

    def _tauN(self, v):
        return(1.0/(self._alphaN(v)+self._betaN(v)))

    def _mInf(self, v):
        return(self._alphaM(v)/(self._alphaM(v)+self._betaM(v)))

    def _tauM(self, v):
        return(1.0/(self._alphaM(v)+self._betaM(v)))

    def _hInf(self, v):
        return(self._alphaH(v)/(self._alphaH(v)+self._betaH(v)))

    def _tauH(self, v):
        return(1.0/(self._alphaH(v)+self._betaH(v)))

    def _alphaN(self, v):
        return(.01*(10-v)/(np.exp((10-v)/10)-1))

    def _betaN(self, v):
        return(.125*np.exp(-v/80.0))

    def _alphaM(self, v):
        return(.1*(25-v)/(np.exp((25-v)/10)-1))

    def _betaM(self, v):
        return(4*np.exp(-v/18.0))

    def _alphaH(self, v):
        return(.07*np.exp(-v/20.0))

    def _betaH(self, v):
        return(1.0/(np.exp((30-v)/10)+1.0))

