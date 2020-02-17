
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel

def main(argv):
    '''
    l = np.array([[.0435, -290.0], [.00015, -1]])
    v1 = np.array([1.0, .00015])
    v2 = np.array([1.0, .0034])
    lambda1 = 0.0
    lambda2 = -.9565

    lv1 = l.dot(v1)
    lv2 = l.dot(v2)
    lambda1v1 = lambda1*v1
    lambda2v2 = lambda2*v2
    pdb.set_trace()
    '''

    '''
    def zeroI(t):
        return 0.0
    model = INapIKModel.getHighThresholdInstance(i=zeroI)
    # model = INapIKModel.getLowThresholdInstance(i=zeroI)
    # vsn = -60.935
    # nsn = .0007
    nVOneHalf = -25.0
    nK = 5.0
    def nInf(v):
        return(1.0/(1.0+np.exp((nVOneHalf-v)/nK)))
    vs = np.arange(-61.0, -59.0, .001)
    ns = nInf(v=vs)
    evals = np.empty((2,len(vs)))
    evals[:] = np.nan
    for i in xrange(len(vs)):
        res = model.checkStability(v0=vs[i], n0=ns[i])
        evals[:,i] = res[1]
    plt.plot(evals[0,:], evals[1,:])
    plt.xlabel(r"$\lambda_0$")
    plt.ylabel(r"$\lambda_1$")
    plt.show()
    pdb.set_trace()
    '''

    '''
    i0 = 4.512865
    v0 = -60.932
    # n0 = .0007
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
    dMInfAtV0 = -1.0/mK*(mInfAtV0-mInfAtV0**2)
    nInfAtV0 = nInf(v=v0)
    n0 = nInf(v=v0)
    gAtV0N0 = (nInfAtV0-n0)/tau
    fAtV0N0 = (i0-gL*(v0-eL)-gNa*mInfAtV0*(v0-eNa)-gK*n0*(v0-eK))/c
    a = (-gL-gNa*(dMInfAtV0*(v0-eNa)+mInfAtV0)-gK*n0)/c
    b = -gK*(v0-eK)/c
    c = (nInfAtV0-nInfAtV0**2)/nK*tau
    d = -1.0/tau
    jacobian = np.array([[a, b], [c, d]])
    eigRes = np.linalg.eig(jacobian)
    pdb.set_trace()
    '''

    # i0 = 4.512865
    # v0 = -60.9325
    i0 = 4.5129
    v0 = -61.0
    # n0 = .000756
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
    n0 = nInf(v=v0)
    gAtV0N0 = (nInfAtV0-n0)/tau
    fAtV0N0 = (i0-gL*(v0-eL)-gNa*mInfAtV0*(v0-eNa)-gK*n0*(v0-eK))/c
    ja = (-gL-gNa*(dMInfAtV0*(v0-eNa)+mInfAtV0)-gK*n0)/c
    jb = -gK*(v0-eK)/c
    jc = (nInfAtV0-nInfAtV0**2)/nK*tau
    jd = -1.0/tau
    jacobian = np.array([[ja, jb], [jc, jd]])
    iJacobian = np.array([[.0435, -290.0], [.00015, -1.0]])
    eigRes = np.linalg.eig(jacobian)
    lambdas = eigRes[0]
    U = eigRes[1]
    UInv = (1.0/np.linalg.det(U))*np.array([[U[1,1],-U[0,1]],[-U[1,0],U[0,0]]])
    # pdb.set_trace()

    def F(x):
        v = x[0]
        n = x[1]
        f1 = (i0-gL*(v-eL)-gNa*mInf(v=v)*(v-eNa)-gK*n*(v-eK))/c
        f2 = (nInf(v=v)-n)/tau
        # pdb.set_trace()
        return(np.array([f1, f2]))
    def FApprox(x):
        xCentered = x-x0
        a = UInv.dot(xCentered)
        fApprox = a[0]*lambdas[0]*U[:,0]+a[1]*lambdas[1]*U[:,1]
        return(fApprox)

    x0 = np.array([v0, n0])
    FAtX0 = F(x=x0)
    x1 = np.array([v0+.01, n0])
    FAtX1 = F(x=x1)
    FApproxAtX1 = FApprox(x=x1)
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
