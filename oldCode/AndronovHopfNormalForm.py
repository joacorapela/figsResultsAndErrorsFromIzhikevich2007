
import numpy as np
import pdb

class AndronovHopfNormalForm:

    def __init__(self, b, cb, wb, a, d):
        self._b = b
        self._cb = cb
        self._wb = wb
        self._a = a
        self._d = d

    def deriv(self, t, y):
        r = y[0]
        phi = y[1]
        aB = self._b(t)
        aCb = self._cb(b=aB)
        aWb = self._wb(b=aB)
        rDot = aCb*r+self._a*r**3
        phiDot = aWb+self._d*r**2
        return(np.array([rDot, phiDot]))
