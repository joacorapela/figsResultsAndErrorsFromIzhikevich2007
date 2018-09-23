

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField

def main(argv):
    plotLowThresholdINapIKVectorField()
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

