

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField
from INapIKExamplePage172ConstantsStore import INapIKExamplePage172ConstantsStore

def main(argv):
    if len(argv)!=6:
        sys.exit("Usage: %s i0 a d aI dI"%argv[0])
    iNapIKLabel = "INap+IK"
    ahNormalFormLabel = "AH Normal Form Rapela"
    iAHNormalFormLabel = "AH Normal Form Izhikevich"
    vAH = INapIKExamplePage172ConstantsStore.vAH
    nAH = INapIKExamplePage172ConstantsStore.nAH
    i0 = float(argv[1])
    a = float(argv[2])
    d = float(argv[3])
    aI = float(argv[4])
    dI = float(argv[5])
    iNapIKResultsFilename = \
     'results/integrationINapIKExampleP172I%.02fa%f.npz'%(i0,a)
    ahNormalFormResultsFilename = \
     'results/integrationAHNormalFormExampleP172I%.02fa%fd%f.npz'%(i0,a,d)
    iAHNormalFormResultsFilename = \
     'results/integrationAHNormalFormExampleP172I%.02fa%fd%f.npz'%(i0,aI,dI)
    voltageFigFilename = \
     'figures/figVoltageExampleP172I%.02fa%fd%faI%fdI%f.eps'%(i0,a,d,aI,dI)
    xlim = (150, 200)
    ylim = (-63, -47)

    ahNormalFormResults = np.load(ahNormalFormResultsFilename)
    iAHNormalFormResults = np.load(iAHNormalFormResultsFilename)
    iNapIKResults = np.load(iNapIKResultsFilename)

    rs = ahNormalFormResults['ys'][0, :]
    phis = ahNormalFormResults['ys'][1, :]
    ahNormalFormVs = vAH + rs*np.cos(phis)

    iRs = iAHNormalFormResults['ys'][0, :]
    iPhis = iAHNormalFormResults['ys'][1, :]
    iAHNormalFormVs = vAH + iRs*np.cos(iPhis)

    plt.plot(iNapIKResults['times'], iNapIKResults['ys'][0, :], 
                                     label=iNapIKLabel)
    iNapIKResults.close()
    plt.plot(ahNormalFormResults['times'], ahNormalFormVs, 
                                           label=ahNormalFormLabel)
    ahNormalFormResults.close()
    plt.plot(iAHNormalFormResults['times'], iAHNormalFormVs, 
                                            label=iAHNormalFormLabel)
    iAHNormalFormResults.close()
    plt.grid()
    plt.xlabel('Time (msec)')
    plt.ylabel('Voltage (mv)')
    plt.legend(loc='upper left')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.savefig(voltageFigFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

