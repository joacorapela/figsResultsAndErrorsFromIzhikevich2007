
import numpy as np
import math
from scipy import signal

import pdb
import matplotlib.pyplot as plt
# from scipy.integrate import ode
from scipy.integrate import odeint

from plotFunctions import plotHighThresholdINapIKVectorField

from signalProcessingUtils import lowpassKaiser

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

# def computeIsochron(model, x0, deltaTs, nInitialConditions, maxDeltaX0, maxDeltaX1, dt=1e-5, vMin=-50.0, vMax=-20.0, tol=1e-3):
def computeIsochron(model, t0, x0, deltaTs, nInitialConditions, maxDistance, dt=1e-5, vMin=-50.0, vMax=-20.0, tol=1e-3):
    isochron = np.empty((len(x0), nInitialConditions*len(deltaTs)))
    isochron[:,0] = x0
    for i in xrange(len(deltaTs)):
        deltaT = deltaTs[i]
        nTSteps = int(math.ceil(deltaT/dt))
        res = integrateForward(deriv=model.deriv, t0=t0, y0=x0, dt=dt, 
                                                  nTSteps=nTSteps)
        x1 = res['ys'][:,-1]
        x1p = np.mean(res['ys'][:,-400:-300], axis=1)
        print("Processing x1=(%.2f,%.4f), (%d/%d)"%(x1[0], x1[1], i+1, len(deltaTs)))
        plt.plot(res['ys'][0,:], res['ys'][1,:])
        plt.annotate("x1", xy=x1, color="red", size=14)
#         initialConditions = chooseRandomNeighbors(x=x1, 
#                                                    nNeighbors=\
#                                                     nInitialConditions, 
#                                                    maxDeltaX0=maxDeltaX0,
#                                                    maxDeltaX1=maxDeltaX1)
        initialConditions = chooseOrthogonalNeighbors(x=x1, 
                                                       xp=x1p,
                                                       nNeighbors=
                                                        nInitialConditions, 
                                                       maxDistance=maxDistance)
        plt.plot(initialConditions[0,:], initialConditions[1,:], marker='o',
color='green', linestyle='None')
        plt.xlim((-90, 15))
        plt.ylim((-0.1, 0.8))
        plt.show()
        pdb.set_trace()
        for j in xrange(initialConditions.shape[1]):
            print('Processing initial condition %d (%d)' % \
                   (j, initialConditions.shape[1]))
            x2 = initialConditions[:,j]
            res = integrateModelBackward(model=model, y0=x2, dt=dt, \
                                          nTSteps=nTSteps)
            # pdb.set_trace()
            isochron[:,i*nInitialConditions+j] = res['ys'][:,-1]
        # pdb.set_trace()
        plt.plot(isochron[0,:], isochron[1,:], marker='o', color='red',
                                linestyle='-')
        plt.xlim((-90, 15))
        plt.ylim((-.1, .8))
    return isochron

def chooseOrthogonalNeighbors(x, xp, nNeighbors, maxDistance):
    v = x-xp
    v = v/math.sqrt(np.inner(v,v))
    w = np.empty(2)
    w[0] = -v[1]
    w[1] = v[0]
    scales = np.arange(-maxDistance, maxDistance, 2.0*maxDistance/nNeighbors)
    neighbors = np.outer(w, scales)+x[:, np.newaxis]
#     plt.arrow(x[0], x[1], v[0], v[1], color="red")
#     plt.arrow(x[0], x[1], w[0], w[1], color="green")
#     pdb.set_trace()
    return neighbors
    
def chooseRandomNeighbors(x, nNeighbors, maxDeltaX0, maxDeltaX1):
    deltaX0s = np.random.uniform(low=-maxDeltaX0/2, high=maxDeltaX0/2, size=nNeighbors)
    deltaX1s = np.random.uniform(low=-maxDeltaX1/2, high=maxDeltaX1/2, size=nNeighbors)
    neighbors = np.array([x[0] + deltaX0s, x[1] + deltaX1s])
    return neighbors

def integrateForward(deriv, t0, y0, dt, nTSteps):
    # integrator = ode(deriv).set_integrator('vode', max_step=dt)
    # integrator.set_initial_value(y0, t0)
    # return integrateIntegrator(integrator=integrator, nTSteps=nTSteps, dt=dt)

    t = np.arange(t0, t0+nTSteps*dt, dt)
    sol = odeint(func=deriv, y0=y0, t=t)
    return {"times":t, "ys":sol.T}

def integrateBackward(deriv, t0, y0, dt, nTSteps):
    # integrator = ode(negativeDeriv).set_integrator('vode', max_step=dt)
    # integrator.set_initial_value(y0, t0)
    # return integrateIntegrator(integrator=integrator, nTSteps=nTSteps, dt=dt)

    t = np.arange(t0, t0-nTSteps*dt, -dt)
    sol = odeint(func=deriv, y0=y0, t=t)
    return {"times":t, "ys":sol.T}

def integrateIntegrator(integrator, nTSteps, dt):
    ys = np.empty((len(integrator.y), nTSteps+1))
    ys[:, 0] = integrator.y

    times = np.empty(nTSteps+1)
    times[0] = integrator.t
    step = 0
    successfulIntegration = True
    t = integrator.t
    y = integrator.y
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

def sortIsochron(isochron, marginStart):
    def euclideanDistance(x, y):
        distance2 = 0
        for i in xrange(len(x)):
            distance2 = distance2 + (x[i]-y[i])**2
        return math.sqrt(distance2)

    def swapColumns(a, i, j):
        aux = np.copy(a[:,i])
        a[:,i] = np.copy(a[:,j])
        a[:,j] = np.copy(aux)

    if marginStart=="maxX":
        minIndex = np.amax(isochron[0,:])
    elif marginStart=="minX":
        minIndex = np.amin(isochron[0,:])
    elif marginStart=="maxY":
        minIndex = np.amax(isochron[1,:])
    elif marginStart=="minY":
        minIndex = np.amin(isochron[1,:])
    else:
        raise ValueError("marginStart should equal minY, maxY, minX, maxX while the %s was given"%(marginIStart))

    if minIndex>0:
        isochron = swapColumns(a=stdIsochron, i=0, j=minIndex)

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

def computePRC(model, nSamples, i0, 
                      waitLC, waitLCPulse, 
                      pulseStrength=5.0, pulseWidthFactor=100, 
                      v0=-60.00, n0=0.0008, t0=0.0, dt = 1e-3, 
                      cutoffHz=4, transitionWidthHz=1.0, rippleDB=60,
                      doPlots=False):
    def computePRCValue(model, dcFristSpikeTimeAfterWaitLCPulse, 
                               dcNSpikesUptoFirstSpikeAfterWaitLCPulse,
                               pulseTime, pulseWidth, pulseStrength, i0, t0, y0,
                               dt, nTSteps, dcTimes, dcVs,
                               cutoffHz, transitionWidthHz, rippleDB,
                               doPlots):
        def iDCPulse(t):
            if pulseTime-pulseWidth/2<t and t<=pulseTime+pulseWidth/2:
                return(i0+pulseStrength)
            return(i0)
        model.setI(i=iDCPulse)
        resDCPulse = integrateForward(deriv=model.deriv, t0=t0,  y0=y0, dt=dt, 
                                                        nTSteps=nTSteps)
        dcPulseV = resDCPulse["ys"][0,:]
        dcPulseFilteredV = lowpassKaiser(x=dcPulseV,
                                          cutoffHz=cutoffHz,
                                          transitionWidthHz=transitionWidthHz,
                                          rippleDB=rippleDB, sampleRate=1/dt,
                                          doPlots=doPlots)
        # begin debug
        # times = resDCPulse["times"]
        # plt.plot(times, dcPulseV, label="original")
        # plt.plot(times, dcPulseFilteredV, label="lowpassed")
        # plt.xlim((100, 103))
        # plt.legend()
        # plt.show()
        # pdb.set_trace()
        # end debug

        dcPulseSpikeIndices = getPeakIndices(v=dcPulseFilteredV)
#         validPeakIndices = \
#          np.nonzero(resDCPulse["ys"][0,peakIndices]>spikeThreshold)[0]
#         peakIndicesAsArray = np.array(peakIndices)
#         dcPulseSpikeIndices = peakIndicesAsArray[validPeakIndices]
#         dcPulseSpikeIndices = peakIndicesAsArray[peakIndices]
        dcPulseSpikeTimes = resDCPulse["times"][dcPulseSpikeIndices]

        dcPulseSpikeTimeAtDCNSpikes = \
         dcPulseSpikeTimes[dcNSpikesUptoFirstSpikeAfterWaitLCPulse-1]
        prcValue = dcFristSpikeTimeAfterWaitLCPulse-dcPulseSpikeTimeAtDCNSpikes

        # start debug
        # plt.plot(dcTimes, dcVs, label="DC")
        # plt.plot(resDCPulse["times"], resDCPulse["ys"][0,:], label="Pulse")
        # plt.axvline(x=pulseTime, color="red")
        # plt.xlabel("Time (ms)")
        # plt.ylabel("Voltage (mV)")
        # plt.legend()
        # plt.show()
        # pdb.set_trace()
        # end debug

        return(prcValue)

    tf = (waitLC+waitLCPulse)*2.0
    nTSteps = int(round((tf-t0)/dt))
    times = np.empty(nTSteps+1)
    pulseWidth = pulseWidthFactor*dt
    def iDC(t):
        return(i0)
    model.setI(i=iDC)
    y0 = np.array([v0, n0])
    resDC = integrateForward(deriv=model.deriv, t0=t0, y0=y0, dt=dt, 
                                               nTSteps=nTSteps)
    # start debug
    # sampleWaitLC=np.argmin(np.abs(resDC["times"]-waitLC))
    # plotHighThresholdINapIKVectorField(i=i0)
    # plt.plot(resDC["ys"][0, :], resDC["ys"][1, :])
    # plt.plot(resDC["ys"][0, sampleWaitLC], resDC["ys"][1, sampleWaitLC], 
    #                                        marker="o", color="red")
    # plt.show()
    # end debug

    dcV = resDC["ys"][0,:]
    dcFilteredV = lowpassKaiser(x=dcV, cutoffHz=cutoffHz,
                                       transitionWidthHz=transitionWidthHz,
                                       rippleDB=rippleDB, sampleRate=1/dt,
                                       doPlots=doPlots)
    dcSpikeIndices = getPeakIndices(v=dcFilteredV)
    dcSpikeTimes = resDC["times"][dcSpikeIndices]
    dcSpikeIndicesAfterWaitLC = np.nonzero(dcSpikeTimes>waitLC)[0]
    dcSpikeTimesAfterWaitLC = dcSpikeTimes[dcSpikeIndicesAfterWaitLC]
    ts = dcSpikeTimesAfterWaitLC[1:]-dcSpikeTimesAfterWaitLC[:-1]
    T = np.mean(ts)

    dcSpikeIndicesAfterWaitLCPulse = np.nonzero(dcSpikeTimes>(waitLC+waitLCPulse))[0]
    dcFristSpikeTimeAfterWaitLCPulse = \
     dcSpikeTimes[dcSpikeIndicesAfterWaitLCPulse[0]]
    dcNSpikesUptoFirstSpikeAfterWaitLCPulse = \
     dcSpikeIndicesAfterWaitLCPulse[0]+1

    # start debug
    # pdb.set_trace()
    # print("mean(T)=%.2f, sd(T)=%.2f"%(T, np.std(ts)))
    # plt.plot(resDC["times"], resDC["ys"][0,:])
    # plt.xlabel("Time (ms)")
    # plt.ylabel("Voltage (mV)")
    # for dcSpikeTime in dcSpikeTimes:
    #     plt.axvline(x=dcSpikeTime, color="black")
    # plt.show()
    # end debug

    phases = np.arange(0, nSamples)*T/nSamples
    pulseTimes = dcSpikeTimesAfterWaitLC[0]+phases
    prc = np.empty(nSamples)
    for i in range(nSamples):
        if i>0:
            print("Processsing phase %d (%d): PRC[%d]=%f"%(i, nSamples, i-1, 
                                                               prc[i-1]))
        else:
            print("Processsing phase %d (%d)"%(i, nSamples))
        prc[i] = computePRCValue(model=model,
                                  dcFristSpikeTimeAfterWaitLCPulse=\
                                   dcFristSpikeTimeAfterWaitLCPulse,
                                  dcNSpikesUptoFirstSpikeAfterWaitLCPulse=
                                   dcNSpikesUptoFirstSpikeAfterWaitLCPulse,
                                  pulseTime=pulseTimes[i],
                                  pulseWidth=pulseWidth,
                                  pulseStrength=pulseStrength,
                                  i0=i0, y0=y0, dt=dt, nTSteps=nTSteps,
                                  dcTimes=resDC["times"],
                                  dcVs=resDC["ys"][0,:],
                                  cutoffHz=cutoffHz, 
                                  transitionWidthHz=transitionWidthHz, 
                                  rippleDB=rippleDB,
                                  doPlots=doPlots)

    # start debug
    # plt.plot(np.arange(0, nSamples)*T/nSamples, prc)
    # plt.xlabel("Phase (ms)")
    # plt.ylabel("Phase Reset (ms)")
    # plt.show()
    # end debug

    return {'prc':prc, 'phases':phases, 'T':T}

def getInterSpikeIntervals(times, vs, sampleRate, cutoffHz=4, 
                                  transitionWidthHz=1.0, rippleDB=60,
                                  doPlots=False):
    filteredVs = lowpassKaiser(x=vs, cutoffHz=cutoffHz,
                                       transitionWidthHz=transitionWidthHz,
                                       rippleDB=rippleDB,
                                       sampleRate=sampleRate,
                                       doPlots=doPlots)
    spikeIndices = getPeakIndices(v=filteredVs)
    spikeTimes = times[spikeIndices]
    ts = spikeTimes[1:]-spikeTimes[:-1]
    return(ts)

def alignMeasurements(times0, measurements0, times1, measurements1):
    # First lets make m0 the longest
    if len(measurements0)>len(measurements1):
        m0 = measurements0
        t0 = times0
        m1 = measurements1
        t1 = times1
        switched = False
    else:
        m0 = measurements1
        t0 = times1
        m1 = measurements0
        t1 = times0
        switched = True

    # Four cases a) m0 start before m1 and m0 finishes after m1
    #            b) m0 start before m1 and m0 finishes before m1
    #            c) m0 start after m1
    #            d) m0 and m1 start at the same time
    if t0[0]<t1[0]:
        index = np.argmin(np.abs(t1[0]-t0))
        if t1[-1]<t0[-1]:
            m0 = m0[index+np.arange(0, len(m1))]
            t0 = t0[index+np.arange(0, len(m1))]
        else:
            m0 = m0[index:]
            t0 = t0[index:]
            m1 = m1[:len(m0)]
            t1 = t1[:len(m0)]
    elif t0[0]>t1[0]:
        index = np.argmin(np.abs(t0[0]-t1))
        m1 = m1[index:]
        t1 = t1[index:]
        m0 = m0[:len(m1)]
        t0 = times0[:len(m1)]
    else: # t0[0]==t1[0]
        m0 = m0[:len(m1)]
        t0 = t0[:len(m1)]
    if switched:
        return {"alignedTimes0":t1, "alignedMeasurements0":m1,
                "alignedTimes1":t0, "alignedMeasurements1":m0}
    else:
        return {"alignedTimes0":t0, "alignedMeasurements0":m0,
                "alignedTimes1":t1, "alignedMeasurements1":m1}


