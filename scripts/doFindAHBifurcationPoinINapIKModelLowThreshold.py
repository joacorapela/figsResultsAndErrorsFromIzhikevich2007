
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel

def main(argv):
    vEqMin = -60
    vEqMax = -50
    vStep = 0.0001
    model = INapIKModel.getLowThresholdInstance(i=None)
    f = model.getFuncVDotAtNInf(i0=0.0)
    vEqs = np.arange(start=vEqMin, stop=vEqMax, step=vStep)
    iEqs = -f(v=vEqs)
    nEqs = model._nInf(v=vEqs)

    realEigValues = np.empty(len(iEqs))
    for i in xrange(len(iEqs)):
        vEq = vEqs[i]
        nEq = nEqs[i]
        jacobian = model.getJacobian(v0=vEq, n0=nEq)
        realEigValues[i] = np.linalg.eig(jacobian)[0][0].real
        
    minEigValueIndex = np.argmin(np.abs(realEigValues))
    print("iAH=%f, vAH=%f, nAH=%f, realEigValues=%f"%\
          (iEqs[minEigValueIndex], vEqs[minEigValueIndex], 
                                   nEqs[minEigValueIndex],
                                   realEigValues[minEigValueIndex],))

    plt.plot(iEqs, realEigValues)
    plt.xlabel('Equilibrium Current')
    plt.ylabel('Real Part of Jacobian Eigenvalues')
    plt.axhline(y=0, color="black")
    plt.axvline(x=iEqs[minEigValueIndex], color="red")
    plt.grid()
    plt.show()

    pdb.set_trace()    

if __name__=="__main__":
    main(sys.argv)
