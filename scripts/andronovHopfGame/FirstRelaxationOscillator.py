

import numpy as np
import pdb

class FirstRelaxationOscillator:

    def __init__(self, f, mu, b):
        self._f = f
        self._mu = mu
        self._b = b

    def deriv(self, t, y):
        v = y[0]
        u = y[1]

        vDot = self._f(v)-u
        uDot = self._mu*(v-self._b)
        return(np.array([vDot, uDot]))

