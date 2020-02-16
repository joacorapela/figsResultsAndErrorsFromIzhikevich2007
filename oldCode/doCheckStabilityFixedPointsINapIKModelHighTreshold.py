
import sys
import pdb
from INapIKModel import INapIKModel

def main(argv):
    i0 = 0.0
    i = lambda t: i0
    c = 1.0
    eL = -80
    gL = 8.0
    gNa = 20.0
    gK = 10.0
    VoneHalf_m = -20.0
    k_m = 15.0
    VoneHalf_n = -25.0
    k_n = 5.0
    eNa = 60.0
    eK = -90
    tau = lambda v: 1.0

    model = INapIKModel(i=i, c=c, gL=gL, eL=eL, gNa=gNa, eNa=eNa, 
                             gK=gK, eK=eK, 
                             mVOneHalf=VoneHalf_m, mK=k_m, 
                             nVOneHalf=VoneHalf_n, nK=k_n, 
                             tau=tau)

    v0Eq1 = -65.9530
    n0Eq1 = 0.0003
    evalsEq1 = model.checkStability(i0=i0, v0=v0Eq1, n0=n0Eq1)
    print("v=%.04f, n=%.04f, eVals="%(v0Eq1, n0Eq1)),evalsEq1

    v0Eq2 = -56.1400
    n0Eq2 = 0.0020
    evalsEq2 = model.checkStability(i0=i0, v0=v0Eq2, n0=n0Eq2)
    print("v=%.04f, n=%.04f, eVals="%(v0Eq2, n0Eq2)),evalsEq2

    v0Eq3 = -27.2805
    n0Eq3 = 0.3879
    evalsEq3 = model.checkStability(i0=i0, v0=v0Eq3, n0=n0Eq3)
    print("v=%.04f, n=%.04f, eVals="%(v0Eq3, n0Eq3)),evalsEq3

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
