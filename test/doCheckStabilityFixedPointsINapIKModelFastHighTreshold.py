
import sys
import pdb
from INapIKModel import INapIKModel

def main(argv):
    i0 = 3.0
    i = lambda v: i0
    c = 1.0
    eL = -80
    gL = 8.0
    gNa = 20.0
    gK = 10.0
    vOneHalf_m = -20.0
    k_m = 15.0
    vOneHalf_n = -25.0
    k_n = 5.0
    eNa = 60.0
    eK = -90
    tau = lambda v: 0.152
    ylim = (-100, 50)

    model = INapIKModel(i=i, c=c, gL=gL, eL=eL, gNa=gNa, eNa=eNa, 
                             gK=gK, eK=eK, 
                             mVOneHalf=vOneHalf_m, mK=k_m, 
                             nVOneHalf=vOneHalf_n, nK=k_n, 
                             tau=tau)
    v0Eq1 = -63.8054
    n0Eq1 = 0.0004
    eValsEq1 = model.checkStability(i0=i0, v0=v0Eq1, n0=n0Eq1)
    v0Eq2 = -58.1365
    n0Eq2 = 0.0013
    eValsEq2 = model.checkStability(i0=i0, v0=v0Eq2, n0=n0Eq2)
    v0Eq3 = -27.1442
    n0Eq3 = 0.3944
    eValsEq3 = model.checkStability(i0=i0, v0=v0Eq3, n0=n0Eq3)

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
