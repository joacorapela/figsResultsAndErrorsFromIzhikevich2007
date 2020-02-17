
import numpy as np
import math
from scipy import signal

import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode

STABLE_NODE = 0
UNSTABLE_NODE = 1
STABLE_FOCUS = 2
UNSTABLE_FOCUS = 3
SADDLE = 4

def buildMatrixFromArraysList(arraysList):
    matrix = np.empty((len(arraysList[0]), len(arraysList)), 
                      dtype=type(arraysList[0][0]))
    matrix[:] = np.nan
    for i in xrange(len(arraysList)):
        matrix[:,i] = arraysList[i]
    return(matrix)

def boltzmann(v, vOneHalf, k):
    return(1.0/(1.0+np.exp((vOneHalf-v)/k)))

def derBoltzmannWRTV(v, vOneHalf, k):
    boltzMannAtV =- boltzmann(v, vOneHalf, k)
    return(boltzMannAtV*(1-boltzMannAtV)/k)

def getStabilityType(eigvals):
    if isinstance(eigvals[0], complex) and isinstance(eigvals[1], complex):
        if eigvals[0].real>=0 and eigvals[1].real>=0:
            return(UNSTABLE_FOCUS)
        elif eigvals[0].real<0 and eigvals[1].real<0:
            return(STABLE_FOCUS)
        else:
            raise ValueError("Invalid eigvals ", eigvals)
    elif eigvals[0]>=0 and eigvals[1]>=0:
        return(UNSTABLE_NODE)
    elif eigvals[0]<0 and eigvals[1]<0:
        return(STABLE_NODE)
    elif (eigvals[0]<0 and eigvals[1]>=0) or \
         (eigvals[0]>=0 and eigvals[1]<0):
        return(SADDLE)
    else:
        raise ValueError("Invalid eigvals ", eigvals)

def computeLimitCycleAmplitudeAndPeriod(xs, times):
    peakIndices = getPeakIndices(v=xs)
    troughIndices = getPeakIndices(v=-xs)
    peaks = xs[peakIndices]
    peakTimes = times[peakIndices]
    troughs = xs[troughIndices]
    troughTimes = times[troughIndices]
    # make sure to have the same number of peaks and troughs
    if len(peaks)>len(troughs):
        peaks = peaks[1:]
        peakTimes = peakTimes[1:]
    else:
        if len(peaks)<len(troughs):
            troughs = troughs[0:-1]
            troughTimes = troughTimes[0:-1]
    amplitudes = (peaks-troughs)/2
    periods = peakTimes[1:]-peakTimes[0:-1]
    medianAmplitudes = np.median(amplitudes)
    sdAmplitudes = np.std(amplitudes)
    medianPeriods = np.median(periods)
    sdPeriods = np.std(periods)
    return {'amplitude':medianAmplitudes, 'sdAmplitudes':sdAmplitudes,
            'period':medianPeriods, 'sdPeriods':sdPeriods}

def getPeakIndices(v, delta=0):
    peakIndices = []
    for i in np.arange(1,(len(v)-1)):
        if v[i-1]+delta<v[i] and v[i]>delta+v[i+1]:
            peakIndices.append(i)


#     plt.plot(v, 'b')
#     maxV = max(v)
#     plt.plot(peakIndices, np.repeat(maxV, len(peakIndices)), 'ro')
#     plt.show()
#     pdb.set_trace()

    return peakIndices

def computeIsochron(model, x0, deltaTs, nInitialConditions, 
                           maxDeltaX0, maxDeltaX1, dt=1e-5,
                           vMin=-50.0, vMax=-20.0, tol=1e-3):
    isochron = np.empty((len(x0), nInitialConditions*len(deltaTs)+2))
    xIntersectionNullclines = model.getIntersectionOfNullclines(vMin=vMin,
                                                                 vMax=vMax,
                                                                 tol=tol)
    isochron[:,0] = xIntersectionNullclines
    isochron[:,1] = x0
    for i in xrange(len(deltaTs)):
        deltaT = deltaTs[i]
        nTSteps = int(math.ceil(deltaT/dt))
        res = integrateModelForward(model=model, y0=x0, dt=dt, nTSteps=nTSteps)
        x1 = res['ys'][:,-1]
        print("Processing x1=(%.2f,%.4f), (%d/%d)"%(x1[0], x1[1], i+1, len(deltaTs)))
        plt.annotate("x1", xy=x1, color="red", size=14)
        initialConditions = chooseRandomNeighbors(x=x1, 
                                                   nNeighbors=\
                                                    nInitialConditions, 
                                                   maxDeltaX0=maxDeltaX0,
                                                   maxDeltaX1=maxDeltaX1)
        plt.plot(initialConditions[0,:], initialConditions[1,:], marker='o',
color='green', linestyle='None')
        # pdb.set_trace()
        for j in xrange(initialConditions.shape[1]):
            print('Processing initial condition %d (%d)' % \
                   (j, initialConditions.shape[1]))
            x2 = initialConditions[:,j]
            res = integrateModelBackward(model=model, y0=x2, dt=dt, \
                                          nTSteps=nTSteps)
            # pdb.set_trace()
            isochron[:,i*nInitialConditions+j+2] = res['ys'][:,-1]
        plt.plot(isochron[0,:], isochron[1,:], marker='o', color='red', linestyle='None')
        plt.xlim((-90, 15))
        plt.ylim((-.1, .8))
        pdb.set_trace()
    return isochron

def chooseRandomNeighbors(x, nNeighbors, maxDeltaX0, maxDeltaX1):
    deltaX0s = np.random.uniform(low=-maxDeltaX0/2, high=maxDeltaX0/2, size=nNeighbors)
    deltaX1s = np.random.uniform(low=-maxDeltaX1/2, high=maxDeltaX1/2, size=nNeighbors)
    neighbors = np.array([x[0] + deltaX0s, x[1] + deltaX1s])
    return neighbors

def integrateModelForward(model, y0, dt, nTSteps):
    integrator = ode(model.deriv).set_integrator('vode', max_step=dt)
    t0 = 0.0
    integrator.set_initial_value(y0, t0)
    return integrateIntegrator(integrator=integrator, nTSteps=nTSteps, dt=dt)

def integrateModelBackward(model, y0, dt, nTSteps):
    def negativeModelDeriv(t, y):
        return -1*model.deriv(t, y)

    integrator = ode(negativeModelDeriv).set_integrator('vode', max_step=dt)
    t0 = 0.0
    integrator.set_initial_value(y0, t0)
    return integrateIntegrator(integrator=integrator, nTSteps=nTSteps, dt=dt)

def integrateIntegrator(integrator, nTSteps, dt):
    ys = np.empty((len(integrator.y), nTSteps+1))
    ys[:, 0] = integrator.y

    times = np.empty(nTSteps+1)
    t = integrator.t
    step = 0
    successfulIntegration = True
    while successfulIntegration and step<nTSteps:
        step = step+1
        """
        if step%100==0:
            print('Processing time %.05f out of %.02f' % (t, tf))
            sys.stdout.flush()
        """
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        times[step] = t
        ys[:, step] = y

    return {'times':times, 'ys':ys}

def sortIsochron(isochron):
    def euclideanDistance(x, y):
        distance2 = 0
        for i in xrange(len(x)):
            distance2 = distance2 + (x[i]-y[i])**2
        return math.sqrt(distance2)

    def swapColumns(a, i, j):
        aux = np.copy(a[:,i])
        a[:,i] = np.copy(a[:,j])
        a[:,j] = np.copy(aux)

    stdIsochron = np.copy(isochron)
    indices = np.ndarray(shape=(1, stdIsochron.shape[1]), dtype=int, buffer=np.arange(stdIsochron.shape[1]))
    for i in xrange(stdIsochron.shape[0]):
        stdIsochron[i,:] = (stdIsochron[i,:]-np.mean(stdIsochron[i,:]))/np.std(stdIsochron[i,:])
    if stdIsochron.shape[1]>2:
        for i in xrange(stdIsochron.shape[1]-1):
            minDistance = euclideanDistance(x=stdIsochron[:,i], 
                                             y=stdIsochron[:,i+1])
            for j in np.arange(i+2, stdIsochron.shape[1]):
                currentDistance = euclideanDistance(x=stdIsochron[:,i], 
                                                     y=stdIsochron[:,j])
                if currentDistance<minDistance:
                    swapColumns(a=stdIsochron, i=i+1, j=j)
                    swapColumns(a=indices, i=i+1, j=j)
                    minDistance = currentDistance
    sortedIsochron = isochron[:, indices[0,:]]
    return(sortedIsochron)

