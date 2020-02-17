
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotStrogatzUnstableLimitCycleVectorField

def getCircleXYs(r, dt):
    thetas = np.arange(0, 2*np.pi, dt)
    xs = r*np.cos(thetas)
    ys = r*np.sin(thetas)
    return({'xs':xs,'ys':ys})

def getTrajectoryXYs(integrationResults):
    rsAndThetas = integrationResults['ys']    
    rs = rsAndThetas[0, :]
    thetas = rsAndThetas[1, :]
    xs = rs*np.cos(thetas)
    ys = rs*np.sin(thetas)
    return({'xs':xs,'ys':ys})

def main(argv):
    mu = -1.0/8.0
    w = 1.0
    b = 1.0
    rUnstableLimitCycle = np.sqrt((1-np.sqrt(1+4*mu))/2) 
    rStableLimitCycle = np.sqrt((1+np.sqrt(1+4*mu))/2)
    # For mu=-1/8 rUnstableLimitCycle=0.38 and rStableLimitCycle=0.92
    inR0 = 0.3
    inTheta0 = np.pi/6
    midR0 = 0.5
    midTheta0 = np.pi/6
    outR0 = 2.0
    outTheta0 = np.pi/6
    limitCycleDt = .01
    colUnstableLimitCycle = "red"
    colStableLimitCycle = "red"
    colTrajectoryIn = "black"
    colTrajectoryMid = "black"
    colTrajectoryOut = "black"
    linewidthStableLimitCycle = 5
    linewidthUnstableLimitCycle = 5
    linestyleStableLimitCycle = "solid"
    linestyleUnstableLimitCycle = "dotted"
    markerStartTrajectory='x'
    markerSizeStartTrajectory=20
    markerColorStartTrajectory="black"
    markerFixedPoint = 'o'
    markerSizeFixedPoint = 75
    facecolorFixedPoint = "red"
    edgecolorFixedPoint = "red"
    resultsIntegrationInFilename = \
     'results/integrationSULCModelMu%.02fR0%.02f.npz'%(mu, inR0)
    resultsIntegrationMidFilename = \
     'results/integrationSULCModelMu%.02fR0%.02f.npz'%(mu, midR0)
    resultsIntegrationOutFilename = \
     'results/integrationSULCModelMu%.02fR0%.02f.npz'%(mu, outR0)
    figFilename = 'figures/strogatzUnstableLimitCyclesMu%.02f.eps'%(mu)

    stableLimitCycleXYs = getCircleXYs(r=rStableLimitCycle, dt=limitCycleDt)
    unstableLimitCycleXYs = getCircleXYs(r=rUnstableLimitCycle, dt=limitCycleDt)
    inIntegrationResults = np.load(resultsIntegrationInFilename)
    inTrajectoryXYs = getTrajectoryXYs(integrationResults=
                                        inIntegrationResults)
    midIntegrationResults = np.load(resultsIntegrationMidFilename)
    midTrajectoryXYs = getTrajectoryXYs(integrationResults=
                                         midIntegrationResults)
    outIntegrationResults = np.load(resultsIntegrationOutFilename)
    outTrajectoryXYs = getTrajectoryXYs(integrationResults=
                                         outIntegrationResults)

    plotStrogatzUnstableLimitCycleVectorField(mu=mu, w=w, b=b, 
                                               xMin=-1.1, xMax=1.1, nXs=50,
                                               yMin=-1.1, yMax=1.1, nYs=50)
    plt.plot(stableLimitCycleXYs['xs'], stableLimitCycleXYs['ys'],
                                        color=colStableLimitCycle,
                                        linestyle=linestyleStableLimitCycle,
                                        linewidth=linewidthStableLimitCycle)
    plt.plot(unstableLimitCycleXYs['xs'], unstableLimitCycleXYs['ys'],
                                          color=colUnstableLimitCycle,
                                          linestyle=linestyleUnstableLimitCycle,
                                          linewidth=linewidthUnstableLimitCycle)
    plt.plot(inTrajectoryXYs['xs'], inTrajectoryXYs['ys'], color=colTrajectoryIn)
    plt.scatter(inR0*np.cos(inTheta0), inR0*np.sin(inTheta0),
                                       s=markerSizeStartTrajectory, 
                                       c=markerColorStartTrajectory,
                                       marker=markerStartTrajectory)
    plt.plot(midTrajectoryXYs['xs'], midTrajectoryXYs['ys'], color=colTrajectoryMid)
    plt.scatter(midR0*np.cos(midTheta0), midR0*np.sin(midTheta0),
                                       s=markerSizeStartTrajectory, 
                                       c=markerColorStartTrajectory,
                                       marker=markerStartTrajectory)
    plt.plot(outTrajectoryXYs['xs'], outTrajectoryXYs['ys'], color=colTrajectoryOut)
    plt.scatter(outR0*np.cos(outTheta0), outR0*np.sin(outTheta0),
                                       s=markerSizeStartTrajectory, 
                                       c=markerColorStartTrajectory,
                                       marker=markerStartTrajectory)
    plt.scatter(0, 0, s=markerSizeFixedPoint, 
                facecolors=facecolorFixedPoint, edgecolors=edgecolorFixedPoint)
    plt.title(r"$\mu$=%.02f"%(mu))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(figFilename)

    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

