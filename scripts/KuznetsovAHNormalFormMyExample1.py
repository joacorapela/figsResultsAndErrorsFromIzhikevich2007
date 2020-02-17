
import numpy as np
import numpy.linalg as linalg

a = np.array([[3, 5], [3, -5]])

aInv = linalg.inv(a)

def h(x):
    y = np.dot(a, x)
    return(y)

def hInv(y):
    x = np.dot(aInv, y)
    return(x)

def hJacobian(x):
    return(a)
