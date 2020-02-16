
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel

def main(argv):
    i0 = 0
    v0 = -70.0
    vf = -50.0
    dv = 1e-3
    deltaAnnotate = 0.3

    def i(t): return(i0)
    iNapIKModel = INapIKModel.getLowThresholdInstance(i=i)
    vs = np.arange(v0, vf, dv)
    lambdasCol = np.empty([len(vs),2], dtype=complex)
    jacobians = []
    vsAll = []
    nsAll = []
    isAll = []
    for j in xrange(len(vs)):
        v = vs[j]
        n = iNapIKModel._nInf(v=vs[j])
        i = iNapIKModel.getIInf(y=(v, n))
        vsAll.append(v)
        nsAll.append(n)
        isAll.append(i)
        _, lambdas, jacobian = iNapIKModel.checkStability(v0=v, n0=n)
        # print(lambdas)
        lambdasCol[j,:] = lambdas
        jacobians.append(jacobian)
    argminEigval0 = np.argmin(np.abs(lambdasCol[:,0].real))
    argminEigval1 = np.argmin(np.abs(lambdasCol[:,1].real))
    # pdb.set_trace()
    if argminEigval0!=argminEigval1:
        raise RuntimeError("Could not find I for which both eigenvalues are zero")
    print("Andronov-Hopft bifurcation I=%f, V=%f, n=%f"%(isAll[argminEigval0],
                                                          vsAll[argminEigval0],
                                                          nsAll[argminEigval0]))
    print("Jacobian at Andronov-Hopft bifurcation point")
    print(jacobians[argminEigval0])
    print("Eigenvalue0=%f+j%f"%(lambdasCol[argminEigval0,0].real,
                                 lambdasCol[argminEigval0,0].imag))
    print("Eigenvalue1=%f+j%f"%(lambdasCol[argminEigval1,1].real,
                                 lambdasCol[argminEigval1,1].imag))
    plt.plot(lambdasCol[:,0].real, lambdasCol[:,1].real)
    plt.xlabel(r"Real($\lambda_0$)")
    plt.ylabel(r"Real($\lambda_1$)")
    plt.annotate('I=%.02f'%isAll[argminEigval0], 
                  xy=(lambdasCol[argminEigval0,0].real, 
                       lambdasCol[argminEigval0,1].real),
                  xytext=(lambdasCol[argminEigval0,0].real-deltaAnnotate,
                           lambdasCol[argminEigval0,1].real+deltaAnnotate),
                  arrowprops=dict(facecolor='black', shrink=0.05))
    plt.grid()
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

