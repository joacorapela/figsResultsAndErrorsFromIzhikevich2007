
import pdb
import numpy as np

def multiplyMatrixColsByScalars(m, s):
    return(m*s.reshape(1, len(s)))

def normalizedCrossCorrelation(x, y):
    answer = np.correlate(x-np.mean(x), y-np.mean(y))[0]
    answer = answer/(np.std(x)*np.std(y))
    return(answer)

def findZeroByBisection(f, xMin, xMax, tol=1e-6):
    if f(xMin)*f(xMax)>0:
        raise ValueError('f(xMin) should be of different sign than f(xMax)')
    if f(xMin)>f(xMax):
        g = lambda x: -f(x)
    else:
        g = f
    # Now g(xMin)<=0<=g(xMax)
    a = xMin
    b = xMax
    while b-a>tol:
        c = a + (b-a)/2
        if g(c)>0:
            b = c
        else:
            a = c
    return(a)

