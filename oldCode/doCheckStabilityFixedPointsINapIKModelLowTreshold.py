
import sys
import pdb
from INapIKModel import INapIKModel

def main(argv):
    i = lambda t: 0.0
    eL = -78.0 
    nVOneHalf = -45.0

    ltINapIKModel = INapIKModel(i=i, eL=eL, nVOneHalf=nVOneHalf)
    ltV0Eq1 = -68.86
    ltN0Eq1 = 0.04
    ltEvalsEq1 = ltINapIKModel.checkStability(v0=ltV0Eq1, n0=ltN0Eq1)

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
