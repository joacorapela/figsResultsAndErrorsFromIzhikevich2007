
import numpy as np
import pdb

class StrogatzUnstableLimitCycleModel:

    def __init__(self, mu, w, b):
        self._mu = mu
        self._w = w
        self._b = b

    def deriv(self, t, y):
        r = y[0]
        theta = y[1]

        rDot = self._mu*r+pow(r, 3)-pow(r, 5)
        thetaDot = self._w+self._b*r**2
        return(np.array([rDot, thetaDot]))
