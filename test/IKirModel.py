
import numpy as np

class IKirModel:
    STABLE = 0
    UNSTABLE = 1
    def __init__(self, i, gL=0.2, eL=-50, gKir=2, eK=-80, vOneHalf=-76, 
                  k=-12, c=1):
        self._i = i
        self._gL = gL
        self._eL = eL
        self._gKir = gKir
        self._eK = eK
        self._vOneHalf = vOneHalf
        self._k = k
        self._c = c

    def deriv(self, t, v):
        f = (self._i(t) - self.getIInf(v=v))/self._c
        return(f)

    def getIInf(self, v):
        i = self._gL*(v-self._eL) + self._gKir*self._hInf(v=v)*(v-self._eK)
        return(i)

    def _hInf(self, v):
        return(1/(1+np.exp((self._vOneHalf-v)/self._k)))

    def _derHInf(self, v):
        hInf = self._hInf(v=v)
        return(hInf/self._k*(1-hInf))

    def checkStability(self, v):
        derFV = -self._gL-\
                 self._gKir*(self._derHInf(v=v)*(v-self._eK)+self._hInf(v=v))
        if derFV<=0:
            return(self.STABLE)
        return(self.UNSTABLE)
