
import pdb
import math
import numpy as np
import scipy.signal as signal
import pylab as plt

def lowpassKaiser(t, x, cutoffHz, transitionWidthHz, rippleDB, sampleRate,
                     doPlots=False):
    nyquistRate = sampleRate/2.0
    width = transitionWidthHz/nyquistRate
    N, beta = signal.kaiserord(rippleDB, width)
    taps = signal.firwin(N, cutoffHz/nyquistRate, window=("kaiser", beta))
    filteredX = signal.lfilter(taps, 1.0, x)
    delay = .5 * (N-1) / sampleRate
    t = np.arange(len(x))/sampleRate
    lowpassedT = t[N-1:]-delay
    lowpassedX = filteredX[N-1:]

    if doPlots:
        # Plot filter coefficients
        plt.figure(1)
        plt.plot(taps, 'bo-', linewidth=2)
        plt.title('Filter Coefficients (%d taps)'%N)
        plt.grid(True)

        # Plot the magnitude response of the filter
        plt.figure(2)
        plt.clf()
        w, h = signal.freqz(taps, worN=8000)
        plt.plot((w/math.pi)*nyquistRate, np.absolute(h), linewidth=2)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain')
        plt.title('Frequency Response')
        plt.ylim(-0.05, 1.05)
        plt.grid(True)

        # Upper inset plot
        ax1 = plt.axes([.42, .6, .45, .25])
        plt.plot((w/math.pi)*nyquistRate, np.absolute(h), linewidth=2)
        plt.xlim(0, 8.0)
        plt.ylim(.9985, 1.001)
        plt.grid(True)

        # Lower inset plot
        ax2 = plt.axes([.42, .25, .45, .25])
        plt.plot((w/math.pi)*nyquistRate, np.absolute(h), linewidth=2)
        plt.xlim(12.0, 20.0)
        plt.ylim(0.0, 0.0025)
        plt.grid(True)

        # plot the original and filtered signals
        plt.figure(3)
        plt.plot(t, x)
        plt.plot(t-delay, filteredX, 'r-')
        plt.plot(t[N-1:]-delay, filteredX[N-1:], 'g', linewidth=4)
        plt.xlabel('t')
        plt.grid(True)
        plt.show()

    return {"t": lowpassedT, "x": lowpassedX}
