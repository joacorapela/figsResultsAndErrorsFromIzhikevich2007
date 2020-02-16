
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel

def main(argv):
    # Full Model
    htINapIKModel = INapIKModel.getHighThresholdInstance(i=None);
    vInfs = np.arange(-72, -51, .1)
    iInfs_fullModel = []
    for vInf in vInfs:
        iInfs_fullModel.append(htINapIKModel.getIInf(v=vInf))
    #

    # Normal Form
    i_sn = 4.512865
    v_sn = -60.9325
    mInfAtV_sn = htINapIKModel._mInf(v=v_sn)
    dMInfAtV_sn = mInfAtV_sn*(1-mInfAtV_sn)/htINapIKModel._mK
    nInfAtV_sn = htINapIKModel._nInf(v=v_sn)
    dNInfAtV_sn = nInfAtV_sn*(1-nInfAtV_sn)/htINapIKModel._nK
    d2IwrtV2AtV_snI_sn = -htINapIKModel._gNa*dMInfAtV_sn*\
                          ((1-2*mInfAtV_sn)*(v_sn-htINapIKModel._eNa)/
                           htINapIKModel._mK+2)\
                          -htINapIKModel._gK*dNInfAtV_sn*\
                           ((1-2*nInfAtV_sn)*(v_sn-htINapIKModel._eK)/
                            htINapIKModel._nK+2)
    nonDegeneracyConstant = 0.5*d2IwrtV2AtV_snI_sn
    transversalityConstant = 1.0/htINapIKModel._c
    iInfs_normalForm = i_sn-\
                        nonDegeneracyConstant/transversalityConstant*\
                         (vInfs-v_sn)**2
    #

    # Plot
    figFilename = "figures/figure6.5.eps"
    plt.plot(iInfs_fullModel, vInfs, label="INapIK")
    plt.plot(iInfs_normalForm, vInfs, label="Normal Form")
    plt.xlabel("Injected DC current, I")
    plt.ylabel("Equilibrium Membrange Voltage, V (mV)")
    plt.legend()
    plt.grid()
    plt.savefig(figFilename)
    plt.show()
    #

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
