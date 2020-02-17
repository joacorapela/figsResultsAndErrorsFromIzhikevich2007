

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField
from INapIKModel import INapIKModel
from INapIKExamplePage172ConstantsStore import INapIKExamplePage172ConstantsStore

def main(argv):
    if len(argv)!=4:
        sys.exit("Usage: %s i0 a d"%argv[0])
    iAH = INapIKExamplePage172ConstantsStore.iAH
    vAH = INapIKExamplePage172ConstantsStore.vAH
    i = lambda t: iAH
    iNapIKModel = INapIKModel.getLowThresholdInstance(i=i)
    nAH = iNapIKModel._nInf(v=vAH)
    i0 = float(argv[1])
    a = float(argv[2])
    d = float(argv[3])
    resultsFilename = 'results/integrationAHNormalFormExampleP172I%.02fa%fd%f.npz'%(i0,a,d)
    phaseFigFilename = 'figures/figPhaseSpaceExampleAHNormalFormP172I%.02fa%fd%f.eps'%(i0,a,d)
    voltageFigFilename = 'figures/figVoltageExampleAHNormalFormP172I%.02fa%fd%f.eps'%(i0,a,d)

    results = np.load(resultsFilename)

    plt.figure()
    # plotLowThresholdINapIKVectorField(i=results['i0'])

    rs = results['ys'][0, :]
    phis = results['ys'][1, :]
    vs = vAH + rs*np.cos(phis)
    ns = nAH + rs*np.sin(phis)

    plt.plot(vs, ns, label="trayectory")
    # axes = plt.gca()
    # ylim = axes.get_ylim()
    # axes.set_ylim((-0.1, ylim[1]))
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.savefig(phaseFigFilename)

    plt.figure()
    plt.plot(results['times'], vs)
    results.close()
    plt.grid()
    plt.xlabel('Time (msec)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

