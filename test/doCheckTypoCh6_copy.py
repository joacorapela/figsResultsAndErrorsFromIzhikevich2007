
import sys
import numpy as np
import pdb
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
    # model = INapIKModel.getHighThresholdInstance(i=zeroI)
    model = INapIKModel.getLowThresholdInstance(i=zeroI)
    isn = 4.51
    vsn = -61.0559
    nsn = .0007
    res = model.checkStability(i0=isn, v0=vsn, n0=nsn)
    pdb.set_trace()
    '''

    v0 = -60.935
    n0 = .0007
    gl = 8.0
    gNa = 20.0
    gK = 10.0
    eNa = 60.0
    mVOneHalf = -20.0
    mK = 15.0
    def mInf(v):
        return(1.0/(1.0+np.exp((mVOneHalf-v)/mK)))
    mInfV0 = mInf(v=v0)
    dMInfV0 = -1.0/mK*(mInfV0-mInfV0**2)
    a = -gl-gNa*(dMInfV0*(v0-eNa)+mInfV0)-gK*n0
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
