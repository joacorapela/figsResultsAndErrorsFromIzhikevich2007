

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField
from INapIKExamplePage172ConstantsStore import INapIKExamplePage172ConstantsStore

def main(argv):
    if len(argv)!=4:
        sys.exit("Usage: %s i0 a d"%argv[0])
    ahNormalFormLabel = "AH Normal Form"
    iNapIKLabel = "INap+IK"
    vAH = INapIKExamplePage172ConstantsStore.vAH
    nAH = INapIKExamplePage172ConstantsStore.nAH
    i0 = float(argv[1])
    a = float(argv[2])
    d = float(argv[3])
    iNapIKResultsFilename = \
     'results/integrationINapIKExampleP172I%.02fa%f.npz'%(i0,a)
    ahNormalFormResultsFilename = \
     'results/integrationAHNormalFormExampleP172I%.02fa%fd%f.npz'%(i0,a,d)
    voltageFigFilename = 'figures/figVoltageExampleP172I%.02fa%fd%f.eps'%(i0,a,d)
    xlim = (150, 200)

    ahNormalFormResults = np.load(ahNormalFormResultsFilename)
    iNapIKResults = np.load(iNapIKResultsFilename)

    rs = ahNormalFormResults['ys'][0, :]
    phis = ahNormalFormResults['ys'][1, :]
    ahNormalFormVs = vAH + rs*np.cos(phis)

    plt.plot(ahNormalFormResults['times'], ahNormalFormVs, 
                                           label=ahNormalFormLabel)
    ahNormalFormResults.close()
    plt.plot(iNapIKResults['times'], iNapIKResults['ys'][0, :], 
                                     label=iNapIKLabel)
    iNapIKResults.close()
    plt.grid()
    plt.xlabel('Time (msec)')
    plt.ylabel('Voltage (mv)')
    plt.legend(loc='upper left')
    plt.xlim(xlim)
    plt.title('a=%f, d=%f'%(a,d))
    plt.savefig(voltageFigFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

