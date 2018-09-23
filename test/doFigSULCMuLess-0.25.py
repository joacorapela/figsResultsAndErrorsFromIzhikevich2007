
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotStrogatzUnstableLimitCycleVectorField

def getTrajectoryXYs(integrationResults):
    rsAndThetas = integrationResults['ys']    
    rs = rsAndThetas[0, :]
    thetas = rsAndThetas[1, :]
    xs = rs*np.cos(thetas)
    ys = rs*np.sin(thetas)
    return({'xs':xs,'ys':ys})

def main(argv):
    mu = -0.5
    w = 1.0
    b = 1.0
    r0 = 2.0
    theta0 = np.pi/6
    limitCycleDt = .01
    colTrajectory = "black"
    markerStartTrajectory='x'
    markerSizeStartTrajectory=20
    markerColorStartTrajectory="black"
    markerFixedPoint = 'o'
    markerSizeFixedPoint = 75
    facecolorFixedPoint = "red"
    edgecolorFixedPoint = "red"
    resultsIntegrationFilename = \
     'results/integrationSULCModelMu%.02fR0%.02f.npz'%(mu, r0)
    figFilename = 'figures/strogatzUnstableLimitCyclesMu%.02f.eps'%(mu)

    integrationResults = np.load(resultsIntegrationFilename)
    trajectoryXYs = getTrajectoryXYs(integrationResults=integrationResults)

    plotStrogatzUnstableLimitCycleVectorField(mu=mu, w=w, b=b, 
                                               xMin=-1.5, xMax=1.5, nXs=50,
                                               yMin=-1.5, yMax=1.5, nYs=50)
    plt.plot(trajectoryXYs['xs'], trajectoryXYs['ys'], color=colTrajectory)
    plt.scatter(r0*np.cos(theta0), r0*np.sin(theta0),
                                   s=markerSizeStartTrajectory, 
                                   c=markerColorStartTrajectory,
                                   marker=markerStartTrajectory)
    plt.scatter(0, 0, s=markerSizeFixedPoint, 
                facecolors=facecolorFixedPoint, edgecolors=edgecolorFixedPoint)
    plt.title(r"$\mu$=%.02f"%(mu))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(figFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

