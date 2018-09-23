
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from utils import computeLimitCycleAmplitudeAndPeriod

def main(argv):
    if len(argv)!=3:
        sys.exit("Usage: %s i0 a"%argv[0])
    i0 = float(argv[1])
    a = float(argv[2])
    resultsFilename = 'results/integrationINapIKExampleP172I%.02fa%f.npz'%(i0,a)
    results = np.load(resultsFilename)
    xs = results['ys'][0,:]
    times = results['times']
    res = computeLimitCycleAmplitudeAndPeriod(xs=xs, times=times)
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

