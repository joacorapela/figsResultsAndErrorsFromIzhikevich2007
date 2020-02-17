
import numpy as np
import pdb

class WeaklyCoupledOscillatorsModel:

    def __init__(self, models, couplings, epsilon, couplingStartTime):
        self._models = models
        self._couplings = couplings
        self._epsilon = epsilon
        self._n = len(models)
        self._couplingStartTime = couplingStartTime

    def deriv(self, y, t):
        m = len(y)/self._n
        aDeriv = np.empty(len(y))
        for i in xrange(self._n):
            indicesI = i*m+np.arange(m)
            if t>=self._couplingStartTime:
                pi = self._getCoupling(y=y, m=m, i=i, indicesI=indicesI)
            else:
                pi = 0.0
            aDeriv[indicesI] = self._models[i].deriv(t=t, y=y[indicesI])+\
                               self._epsilon*pi
        return(aDeriv)

    def _getCoupling(self, y, m, i, indicesI):
        pi = 0
        for j in xrange(self._n):
            indicesJ = j*m+np.arange(m)
            pi = pi + self._couplings[i][j](x1=y[indicesI], x2=y[indicesJ])
        return(pi)
