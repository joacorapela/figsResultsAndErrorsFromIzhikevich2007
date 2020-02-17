

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField

def main(argv):
    figFilename = 'figures/fig4-4.eps'
    plotLowThresholdINapIKVectorField()
    plt.savefig(figFilename)
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

