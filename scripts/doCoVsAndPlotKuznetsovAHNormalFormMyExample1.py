

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from KuznetsovAHNormalFormMyExample1 import h

def main(argv):
    if len(argv)!=5:
        sys.exit("Usage: %s beta0 sign x10 x20"%argv[0])
    beta = float(argv[1])
    sign = float(argv[2])
    x10 = float(argv[3])
    x20 = float(argv[4])
    resultsFilename = \
     'results/integrationKuznetsovAHNormalFormMyExample1Beta%.02fSign%dX10%.02fX20%.02f.npz'%(beta,sign,x10,x20)
    phaseFigFilename = \
     'figures/figPhaseSpaceCoVsOnKuznetsovAHNormalMyExample1Beta%.02fSign%dX10%.02fX20%.02f.eps'%(beta,sign,x10,x20)

    results = np.load(resultsFilename)

    plt.figure()

    ys = h(x=results['ys'])

    plt.plot(ys[0,:], ys[1,:], label="trayectory")
    plt.grid()
    plt.legend()
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.savefig(phaseFigFilename)

    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

