
import numpy as np
import pdb
from KuznetsovAHNormalForm import KuznetsovAHNormalForm

class KuznetsovAHNormalFormWithCoVs:

    def __init__(self, beta, sign, hJacobian, hInv):
        self._kAHNormalForm = KuznetsovAHNormalForm(beta=beta, sign=sign)
        self._hJacobian = hJacobian
        self._hInv = hInv

    def deriv(self, t, y):
        x = self._hInv(y=y)
        yDot = np.dot(self._hJacobian(x=x), 
                       self._kAHNormalForm.deriv(t=0, y=x))
        return(yDot)
