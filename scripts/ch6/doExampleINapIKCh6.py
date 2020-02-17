
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel

def main(argv):
    i0 = 4.512865
    v0 = -60.9325
    n0 = .000756
    c = 1.0
    gL = 8.0
    gNa = 20.0
    gK = 10.0
    eL = -80.0
    eNa = 60.0
    eK = -90.0
    mVOneHalf = -20.0
    mK = 15.0
    nVOneHalf = -25.0
    nK = 5.0
    tau = 1.0
    def mInf(v):
        return(1.0/(1.0+np.exp((mVOneHalf-v)/mK)))
    def nInf(v):
        return(1.0/(1.0+np.exp((nVOneHalf-v)/nK)))
    mInfAtV0 = mInf(v=v0)
    dMInfAtV0 = mInfAtV0*(1-mInfAtV0)/mK
    nInfAtV0 = nInf(v=v0)
    dNInfAtV0 = nInfAtV0*(1-nInfAtV0)/nK
    gAtV0N0 = (nInfAtV0-n0)/tau
    fAtV0N0 = (i0-gL*(v0-eL)-gNa*mInfAtV0*(v0-eNa)-gK*n0*(v0-eK))/c
    ja = (-gL-gNa*(dMInfAtV0*(v0-eNa)+mInfAtV0)-gK*n0)/c
    jb = -gK*(v0-eK)/c
    jc = (nInfAtV0-nInfAtV0**2)/nK*tau
    jd = -1.0/tau
    jacobian = np.array([[ja, jb], [jc, jd]])
    eigRes = np.linalg.eig(jacobian)
    lambdas = eigRes[0]
    U = eigRes[1]

    d2IwrtV2AtV0I0 = -gNa*dMInfAtV0*((1-2*mInfAtV0)*(v0-eNa)/mK+2)\
                     -gK*dNInfAtV0*((1-2*nInfAtV0)*(v0-eK)/nK+2)
    a = 0.5*d2IwrtV2AtV0I0

    print("Jacobian")
    print(jacobian)
    print("Jacobian eigenvalues")
    print(lambdas)
    print("Jacobian eigenvectors")
    print(U)
    print("a=%f"%(a))
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
