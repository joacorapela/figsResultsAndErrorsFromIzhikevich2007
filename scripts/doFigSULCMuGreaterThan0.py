
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
    mu = 1.0
    w = 1.0
    b = 1.0
    inR0 = 0.1
    inTheta0 = np.pi/6
    outR0 = 2.0
    outTheta0 = np.pi/6
    rStableLimitCycle = np.sqrt((1+np.sqrt(1+4*mu))/2)
    limitCycleDt = .01
    colStableLimitCycle = "red"
    colTrajectoryOut = "black"
    colTrajectoryIn = "black"
    linewidthLimitCycle = 5
    markerStartTrajectory='x'
    markerSizeStartTrajectory=20
    markerColorStartTrajectory="black"
    markerFixedPoint = 'o'
    markerSizeFixedPoint = 75
    facecolorFixedPoint = "none"
    edgecolorFixedPoint = "red"
    resultsIntegrationInFilename = \
     'results/integrationSULCModelMu%.02fR0%.02f.npz'%(mu, inR0)
    resultsIntegrationOutFilename = \
     'results/integrationSULCModelMu%.02fR0%.02f.npz'%(mu, outR0)
    figFilename = 'figures/strogatzUnstableLimitCyclesMu%.02f.eps'%(mu)

    stableLimitCycleXYs = getCircleXYs(r=rStableLimitCycle, dt=limitCycleDt)
    inIntegrationResults = np.load(resultsIntegrationInFilename)
    inTrajectoryXYs = getTrajectoryXYs(integrationResults=inIntegrationResults)
    outIntegrationResults = np.load(resultsIntegrationOutFilename)
    outTrajectoryXYs = getTrajectoryXYs(integrationResults=
                                         outIntegrationResults)

    plotStrogatzUnstableLimitCycleVectorField(mu=mu, w=w, b=b, 
                                               xMin=-1.5, xMax=1.5, nXs=50,
                                               yMin=-1.5, yMax=1.5, nYs=50)
    plt.plot(stableLimitCycleXYs['xs'], stableLimitCycleXYs['ys'], color=colStableLimitCycle, linewidth=linewidthLimitCycle)
    plt.plot(inTrajectoryXYs['xs'], inTrajectoryXYs['ys'], color=colTrajectoryIn)
    plt.scatter(inR0*np.cos(inTheta0), inR0*np.sin(inTheta0),
                                       s=markerSizeStartTrajectory, 
                                       c=markerColorStartTrajectory,
                                       marker=markerStartTrajectory)
    plt.plot(outTrajectoryXYs['xs'], outTrajectoryXYs['ys'], color=colTrajectoryOut)
    plt.scatter(0, 0, s=markerSizeFixedPoint, 
                facecolors=facecolorFixedPoint, edgecolors=edgecolorFixedPoint)
    plt.scatter(outR0*np.cos(outTheta0), outR0*np.sin(outTheta0),
                                       s=markerSizeStartTrajectory, 
                                       c=markerColorStartTrajectory,
                                       marker=markerStartTrajectory)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(r"$\mu$=%.02f"%(mu))
    plt.savefig(figFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

