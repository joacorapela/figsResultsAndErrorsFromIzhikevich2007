
import numpy as np
import pdb

class MalkinsPhaseDeviationModelOfWeaklyCoupledOscillators:

    def __init__(self, hs, epsilon):
        self._hs = hs
        self._epsilon = epsilon

    def deriv(self, y, t):
        print("deriv at y=(%.02f, %.02f), t=%.02f"%(y[0],y[1],t))
        answer = np.empty(len(y))
        for i in xrange(len(y)):
            aSum = 0.0
            for j in xrange(len(y)):
                phaseDiff = y[j]-y[i]
                aSum = aSum + self._hs[i][j](phaseDiff=phaseDiff)
            answer[i] = self._epsilon*aSum
        return answer
