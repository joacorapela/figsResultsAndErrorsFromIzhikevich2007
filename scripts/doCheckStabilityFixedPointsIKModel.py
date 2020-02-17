
import sys
import pdb
from IKModel import IKModel
import utils

def main(argv):
    i0 = 0.0
    i = lambda t: 0.0

    ikModel = IKModel(i=i)
    v0Eq1 = -80.004
    m0Eq1 = 0.1418
    checkStabilityRes = ikModel.checkStability(i0=i0, v0=v0Eq1, m0=m0Eq1)

    if(checkStabilityRes[0]==utils.STABLE_NODE):
        print("STABLE_NODE")
    elif(checkStabilityRes[0]==utils.UNSTABLE_NODE):
        print("UNSTABLE_NODE")
    elif(checkStabilityRes[0]==utils.STABLE_FOCUS):
        print("STABLE_FOCUS")
    elif(checkStabilityRes[0]==utils.UNSTABLE_FOCUS):
        print("UNSTABLE_FOCUS")
    elif(checkStabilityRes[0]==utils.SADDLE):
        print("SADDLE")
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
