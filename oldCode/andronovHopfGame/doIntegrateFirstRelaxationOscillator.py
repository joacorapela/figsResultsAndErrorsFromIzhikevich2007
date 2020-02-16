
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from FirstRelaxationOscillator import FirstRelaxationOscillator

def main(argv):
    mu = 1.0

    '''
    # Supercritical. After loss stability. Outside stable limit cycle
    f = lambda x: -np.exp(x)*x**2
    fPrime = lambda x: f(x)-2*np.exp(x)*x
    b = -0.1
    deltaU0 = .5
    deltaV0 = .5
    tf = 50.0
    traceCol = 'grey'
    resultsFilename = 'results/integrationFirstRelaxationOscillatorSupercriticalAfterLossOfStabilityStartOutsideStableLC.npz'
    figFilename = 'figures/phaseSpaceFirstRelaxationOscillatorSupercriticalAfterLossOfStabilityStartOutsideStableLC.eps'
    '''

    '''
    # Supercritical. After loss stability. Inside stable limit cycle
    f = lambda x: -np.exp(x)*x**2
    fPrime = lambda x: f(x)-2*np.exp(x)*x
    b = -0.1
    deltaU0 = .05
    deltaV0 = .05
    tf = 50.0
    traceCol = 'grey'
    resultsFilename = 'results/integrationFirstRelaxationOscillatorSupercriticalAfterLossOfStabilityStartInsideStableLC.npz'
    figFilename = 'figures/phaseSpaceFirstRelaxationOscillatorSupercriticalAfterLossOfStabilityStartInsideStableLC.eps'
    '''

    '''
    # Supercritical. Before loss stability.
    f = lambda x: -np.exp(x)*x**2
    fPrime = lambda x: f(x)-2*np.exp(x)*x
    b = 0.1
    deltaU0 = .4
    deltaV0 = .4
    tf = 15.0
    traceCol = 'blue'
    resultsFilename = 'results/integrationFirstRelaxationOscillatorSupercriticalBeforeLossOfStability.npz'
    figFilename = 'figures/phaseSpaceFirstRelaxationOscillatorSupercriticalBeforeLossOfStability.eps'
    '''

    '''
    # Subcritical. After loss stability.
    f = lambda x: np.exp(x)*x**2
    fPrime = lambda x: f(x)+2*np.exp(x)*x
    b = 0.1
    deltaU0 = .05
    deltaV0 = .05
    tf = 15.0
    traceCol = 'red'
    resultsFilename = 'results/integrationFirstRelaxationOscillatorSubcriticalAfterLossOfStability.npz'
    figFilename = 'figures/phaseSpaceFirstRelaxationOscillatorSubcriticalAfterLossOfStability.eps'
    '''

    # Subcritical. Before loss stability. Start inside unstable limit cycle.
    f = lambda x: np.exp(x)*x**2
    fPrime = lambda x: f(x)+2*np.exp(x)*x
    b = -0.1
    deltaU0 = .4
    deltaV0 = .4
    tf = 30.0
    traceCol = 'grey'
    resultsFilename = 'results/integrationFirstRelaxationOscillatorSubcriticalBeforeLossOfStabilityStartInsideUnstableLC.npz'
    figFilename = 'figures/phaseSpaceFirstRelaxationOscillatorSubcriticalBeforeLossOfStabilityStartInsideUnstableLC.eps'

    '''
    # Subcritical. Before loss stability. Start outside unstable limit cycle.
    f = lambda x: np.exp(x)*x**2
    fPrime = lambda x: f(x)+2*np.exp(x)*x
    b = -0.1
    deltaU0 = .5
    deltaV0 = .5
    tf = 15.0
    traceCol = 'grey'
    resultsFilename = 'results/integrationFirstRelaxationOscillatorSubcriticalBeforeLossOfStabilityStartOutsideUnstableLC.npz'
    figFilename = 'figures/phaseSpaceFirstRelaxationOscillatorSubcriticalBeforeLossOfStabilityStartOutsideUnstableLC.eps'
    '''

    t0 = 0.0
    # tf = 12.50
    dt = 1e-3
    eqMarker = 'o'
    eqCol = 'grey'
    eqSize = 8
    startMarker = 'x'
    startCol = 'red'
    startSize = 8
    traceMarker = '.'
    traceSize = 1
    xlim = (-1, 1)
    ylim = (-1, 1)
    vEq = b
    uEq = f(b)
    if f(b)**2<4*mu:
        realEig1 = realEig2 = fPrime(b)/2
    else:
        eig1 = (fPrime(b)+np.sqrt(fPrime(b)**2-4*mu))/2
        eig2 = (fPrime(b)-np.sqrt(fPrime(b)**2-4*mu))/2
        realEig1 = eig1
        realEig2 = eig2
    if realEig1<0 and realEig2<0:
        stableEq = True
        print("Stable equilibrium at vEq=%.2f and uEq=%.2f"%(vEq, uEq))
    else:
        stableEq = False
        print("Unstable equilibrium at vEq=%.2f and uEq=%.2f"%(vEq, uEq))

    raw_input("Press any key to continue:")

    v0 = vEq+deltaV0
    u0 = uEq+deltaU0
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    model = FirstRelaxationOscillator(f=f, mu=mu, b=b)
    integrator = ode(model.deriv).set_integrator('vode')

    y0 = np.array([v0, u0])
    integrator.set_initial_value(y0, t0)
    ys = np.empty((2, nTSteps+1))
    ys[:, 0] = y0

    t = t0
    step = 0
    successfulIntegration = True
    while successfulIntegration and step<nTSteps:
        step = step+1
        if step%100==0:
            print('Processing time %.05f out of %.02f: y=[%.2f, %.2f]' % 
                  (t, tf, ys[0, step-1], ys[1, step-1]))
            sys.stdout.flush()
            # pdb.set_trace()
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        times[step] = t
        ys[:, step] = y

    np.savez(resultsFilename, times=times, ys=ys)

    if stableEq:
        plt.plot(vEq, uEq, color=eqCol, marker=eqMarker, 
                      markerfacecolor=eqCol, markersize=eqSize)
    else:
        plt.plot(vEq, uEq, color=eqCol, marker=eqMarker,
                      markerfacecolor='none', markersize=eqSize)
    plt.plot(v0, u0, color=startCol, marker=startMarker, markersize=startSize)
    plt.plot(ys[0, :], ys[1, :], color=traceCol, marker=traceMarker,
                       markersize=traceSize)
    plt.grid()
    plt.xlabel('v')
    plt.ylabel('u')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

