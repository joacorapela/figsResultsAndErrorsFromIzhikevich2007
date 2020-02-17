
import sys
import numpy as np
import pdb
from INapIKModel import INapIKModel
from AndronovHopfNormalFormCalculator import AndronovHopfNormalFormCalculator
from INapIKExamplePage172ConstantsStore import INapIKExamplePage172ConstantsStore

def main(argv):
    v0 = INapIKExamplePage172ConstantsStore.vAH
    i0 = INapIKExamplePage172ConstantsStore.iAH
    iNapIKModel = INapIKModel.getLowThresholdInstance(i=i0)
    n0 = iNapIKModel._nInf(v=v0)
    # test code
    # jacobian = iNapIKModel.getJacobian(v0=v0, n0=n0)
    # eigRes = np.linalg.eig(a=jacobian)
    # pdb.set_trace()
    #

    def getJacobianFunc(alpha):
        iInf = i0+alpha
        vs = np.arange(-100, 0, .1)
        iNapIKModel = INapIKModel.getLowThresholdInstance(i=None)
        iInfs = iNapIKModel.getIInf(v=vs)
        matchIndex = np.argmin(np.abs(iInfs-iInf))
        vInfForAlpha = vs[matchIndex]
        nInfForAlpha = iNapIKModel._nInf(v=vInfForAlpha)
        jacobian = iNapIKModel.getJacobian(v0=vInfForAlpha, n0=nInfForAlpha)
        return(jacobian)

    mInf = iNapIKModel._mInf
    nInf = iNapIKModel._nInf
    c = iNapIKModel._c
    mK = iNapIKModel._mK
    nK = iNapIKModel._nK
    gL = iNapIKModel._gL
    gNa = iNapIKModel._gNa
    gK = iNapIKModel._gK
    eL = iNapIKModel._eL
    eNa = iNapIKModel._eNa
    eK = iNapIKModel._eK
    tau = iNapIKModel._tau(v=0)
    mInfAtV0 = mInf(v=v0)
    dMInfAtV0 = mInfAtV0/mK*(1-mInfAtV0)
    d2MInfAtV0 = dMInfAtV0/mK*(1-2*mInfAtV0)
    d3MInfAtV0 = d2MInfAtV0/mK*(1-2*mInfAtV0)-2*dMInfAtV0**2/mK
    nInfAtV0 = nInf(v=v0)
    dNInfAtV0 = nInfAtV0/nK*(1-nInfAtV0)
    d2NInfAtV0 = dNInfAtV0/nK*(1-2*nInfAtV0)
    d3NInfAtV0 = d2NInfAtV0/nK*(1-2*nInfAtV0)-2*dNInfAtV0**2/nK
    d2F1dX12At000 = 1.0/c*-gNa*(d2MInfAtV0*(v0-eNa)+2*dMInfAtV0)
    d2F1dX1dX2At000 = -gK
    d2F1dX22At000 = 0.0
    d3F1dX13At000 = 1.0/c*-gNa*(d3MInfAtV0*(v0-eNa)+3*d2MInfAtV0)
    d3F1dX12dX2At000 = 0.0
    d3F1dX1dX22At000 = 0.0
    d3F1dX23At000 = 0.0
    d2F2dX12At000 = d2NInfAtV0
    d2F2dX1dX2At000 = 0.0
    d2F2dX22At000 = 0.0
    d3F2dX13At000 = d3NInfAtV0
    d3F2dX12dX2At000 = 0.0
    d3F2dX1dX22At000 = 0.0
    d3F2dX23At000 = 0.0
    alpha = -2.0

    ahnfCalc = AndronovHopfNormalFormCalculator()
    res = ahnfCalc.computeNormalForm(getJacobianFunc=getJacobianFunc,
                                      d2F1dX12At000=d2F1dX12At000,
                                      d2F1dX1dX2At000=d2F1dX1dX2At000,
                                      d2F1dX22At000=d2F1dX22At000,
                                      d3F1dX13At000=d3F1dX13At000,
                                      d3F1dX12dX2At000=d3F1dX12dX2At000,
                                      d3F1dX1dX22At000=d3F1dX1dX22At000,
                                      d3F1dX23At000=d3F1dX23At000,
                                      d2F2dX12At000=d2F2dX12At000,
                                      d2F2dX1dX2At000=d2F2dX1dX2At000,
                                      d2F2dX22At000=d2F2dX22At000,
                                      d3F2dX13At000=d3F2dX13At000,
                                      d3F2dX12dX2At000=d3F2dX12dX2At000,
                                      d3F2dX1dX22At000=d3F2dX1dX22At000,
                                      d3F2dX23At000=d3F2dX23At000,
                                      alpha=alpha)
    beta = res[0]
    s = res[1]
    print("beta=%f, s=%d"%(beta, s))
    pdb.set_trace()
    
if __name__ == "__main__":
    main(sys.argv)

