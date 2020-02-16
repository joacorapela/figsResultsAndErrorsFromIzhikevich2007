
import math

class INapModel:

    def __init__(self, i, gL=19, eL=-67, gNa=74, eNa=60, vOneHalf=1.5, 
                  k=16, c=10):
        self._i = i
        self._gL = gL
        self._eL = eL
        self._gNa = gNa
        self._eNa = eNa
        self._vOneHalf = vOneHalf
        self._k = k
        self._c = c

    def deriv(self, t, v):
        f = (self._i(t) - self.getIInf(v=v))/self._c
        return(f)

    def getIInf(self, v):
        i = self._gL*(v-self._eL) + self._gNa*self._mInf(v=v)*(v-self._eNa)
        return(i)

#     def deriv(self, t, v):
#         f = (self._i(t) - self._gL*(v-self._eL)
#                         - self._gNa*self._mInf(v=v)*(v-self._eNa))/self._c
#         return(f)

    def _mInf(self, v):
        return(1/(1+math.exp((self._vOneHalf-v)/self._k)))
