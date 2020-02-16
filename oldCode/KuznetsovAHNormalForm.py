
import numpy as np
import pdb

class KuznetsovAHNormalForm:

    def __init__(self, beta, sign):
        if abs(sign)!=1:
            raise ValueError('sign must equal +/-1')
        self._beta = beta
        self._sign = sign

    def deriv(self, t, y):
        x1 = y[0]
        x2 = y[1]
        x1Dot = self._beta*x1-x2+self._sign*(x1**2+x2**2)*x1
        x2Dot = x1+self._beta*x2+self._sign*(x1**2+x2**2)*x2
        return(np.array([x1Dot, x2Dot]))
