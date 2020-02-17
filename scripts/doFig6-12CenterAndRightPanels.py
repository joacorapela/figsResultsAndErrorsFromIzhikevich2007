
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKExamplePage172ConstantsStore import INapIKExamplePage172ConstantsStore
from utils import computeLimitCycleAmplitudeAndPeriod

def main(argv):
    if len(argv)!=5:
        sys.exit("Usage: %s a d aI dI"%argv[0])
    a = float(argv[1])
    d = float(argv[2])
    aI = float(argv[3])
    dI = float(argv[4])
    i0s = np.arange(15, 20, .25)
    i0s = np.insert(i0s, 0, 14.67)
    resultsFilenamePattern = "results/integrationINapIKExampleP172I%.02fa%f.npz"
    ampsFigFilename = "figures/ampsFig6-12a%.04fd%.04faI%.04fdI%.04f.eps"%(a,
d, aI, dI)
    freqsFigFilename = "figures/freqsFig6-12a%.04fd%.04faI%.04fdI%.04f.eps"%(a,
d, aI, dI)
    resT = getTheoreticalAmplitudesAndFreqs(a=a, d=d, i0s=i0s)
    resTI = getTheoreticalAmplitudesAndFreqs(a=aI, d=dI, i0s=i0s)
    resN = getNumericalAmplitudesAndFreqs(a=a, d=d, i0s=i0s, resultsFilenamePattern=resultsFilenamePattern)

    plt.figure()
    plt.plot(i0s, resN["amplitudes"], label="numerical", marker="o")
    plt.plot(i0s, resT["amplitudes"], label="theoretical Rapela", marker="+")
    plt.plot(i0s, resTI["amplitudes"], label="theoretical Izhikevich", marker="x")
    plt.xlabel("injected dc-current, I")
    plt.ylabel("membrane voltage (mv)")
    plt.legend(loc="upper left")
    plt.savefig(ampsFigFilename)

    plt.figure()
    plt.plot(i0s, resN["freqs"], label="numerical", marker="o")
    plt.plot(i0s, resT["freqs"], label="theoretical Rapela", marker="+")
    plt.plot(i0s, resTI["freqs"], label="theoretical Izhikevich", marker="x")
    plt.xlabel("Injected dc-current, I")
    plt.ylabel(r"frequency, 2$\pi$/period (radians/ms)")
    plt.legend(loc="upper left")
    plt.savefig(freqsFigFilename)

    plt.show()
    pdb.set_trace()

def getNumericalAmplitudesAndFreqs(a, d, i0s, resultsFilenamePattern):
    amplitudes = np.empty(len(i0s))
    freqs = np.empty(len(i0s))
    for i in xrange(len(i0s)):
        i0 = i0s[i]
        resultsFilename = resultsFilenamePattern%(i0,a)
        results = np.load(resultsFilename)
        xs = results["ys"][0,:]
        times = results["times"]
        res = computeLimitCycleAmplitudeAndPeriod(xs=xs, times=times)
        amplitudes[i] = res["amplitude"]
        freqs[i] = 2*np.pi/res["period"]
    return {"amplitudes":amplitudes, "freqs":freqs}

def getTheoreticalAmplitudesAndFreqs(a, d, i0s):
    amplitudes = np.empty(len(i0s))
    freqs = np.empty(len(i0s))
    for i in xrange(len(i0s)):
        b = i0s[i]
        cb = lambda b: 0.0307*(b-INapIKExamplePage172ConstantsStore.iAH)
        wb = lambda b: 2.1376+0.0407*(b-INapIKExamplePage172ConstantsStore.iAH)
        amplitudes[i] = np.sqrt(cb(b)/abs(a))
        freqs[i] = wb(b)+d*cb(b)/abs(a)
    return {"amplitudes":amplitudes, "freqs":freqs}

if __name__ == "__main__":
    main(sys.argv)

