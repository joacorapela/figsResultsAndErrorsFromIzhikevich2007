
import sys
import pdb
import math
import matplotlib.pyplot as plt
import numpy as np
from plotFunctions import plotVectorField

def main(argv):
    a = 24.0
    b = 11.0
    c = 1.0
    x0 = 3.0
    y0 = 33.5
    integrationResultsFilename = "results/integrationA%fB%fC%fX0%fY0%f.npz"%\
                                  (a, b, c, x0, y0)
    figFilename = "figures/unstableNodeA%fB%fC%fX0%fY0%f.eps"%(a, b, c, x0, y0)
    xMin = 0.0
    xMax = 10.0
    nXs = 16 
    yMin = 10.0
    yMax = 150.0
    nYs=16
    colorSaddle = (1.0, 0.0, 0.0)
    colorSaddleNode = (0.5, 0.0, 0.0)
    colorStableNode = (0.0, 1.0, 0.0)
    colorStableFocus = (0.0, 0.5, 0.0)
    colorUnstableNode = (0.0, 0.0, 1.0)
    colorUnstableFocus = (0.0, 0.0, 0.5)
    
    if a>0.25*(b/c)**2:
        print("No real equilibria")
        return()

    xe1 = (b/c+math.sqrt((b/c)**2-4*a))/2.0
    ye1 = b/c*xe1

    if a==0.25*(b/c)**2:
        e1Type = "saddle-node"
        e1Color = colorSaddleNode
        print("(%f,%f) is a saddle-node"%(xe1,ye1))
    else:
        e1Type = "saddle"
        e1Color = colorSaddle
        print("(%f,%f) is a saddle"%(xe1,ye1))

    xe2 = (b/c-math.sqrt((b/c)**2-4*a))/2.0
    ye2 = b/c*xe2

    if a==0.25*(b/c)**2:
        if b==c**2:
            raise NotImplementedError()
        else:
            e2Type = "saddle-node"
            e2Color = colorSaddleNode
            print("(%f,%f) is a saddle-node"%(xe2,ye2))

    tau2 = b/c-math.sqrt((b/c)**2-4*a)-c
    delta2 = c*math.sqrt((b/c)**2-4*a)
    if b<=c**2 or a<(2*b-c**2)/4:
        if tau2**2<4*delta2:
            e2Type = "stable focus"
            e2Color = colorStableFocus
            print("(%f,%f) is a stable focus"%(xe2,ye2))
        else:
            e2Type = "stable node"
            e2Color = colorStableNode
            print("(%f,%f) is a stable node"%(xe2,ye2))
    elif a>(2*b-c**2)/4:
        if a==0.25*(b/c)**2:
            raise NotImplementedError()
        if tau2**2<4*delta2:
            e2Type = "unstable focus"
            e2Color = colorUnstableFocus
            print("(%f,%f) is a unstable focus"%(xe2,ye2))
        else:
            e2Type = "unstable node"
            e2Color = colorUnstableNode
            print("(%f,%f) is a unstable node"%(xe2,ye2))

    f = lambda x, y: a+x**2-y
    g = lambda x, y: b*x-c*y
    results = np.load(integrationResultsFilename)
    xs = np.arange(xMin, xMax, (xMax-xMin)/nXs)
    ys = np.arange(yMin, yMax, (yMax-yMin)/nYs)
    plotVectorField(xDotFun=f, yDotFun=g, 
                               xMin=xMin, xMax=xMax, nXs=nXs, 
                               yMin=yMin, yMax=yMax, nYs=nYs)
    plt.scatter(xe1, ye1, marker="o", label=e1Type, color=e1Color)
    plt.scatter(xe2, ye2, marker="o", label=e2Type, color=e2Color)
    plt.plot(results['zs'][0, :], results['zs'][1, :], color="orange", 
                                  label="trajectory")
    plt.scatter(x0, y0, marker="x", color="orange")
    plt.axvline(c/2, color="black", linestyle=":")
    plt.plot(xs, b/c*xs, color="blue", label="y nullcline")
    plt.plot(xs, a+xs**2, color="red", label="x nullcline")
    plt.axvline(c/2, color="black", linestyle=":")
    yDelta = (yMax-yMin)/nXs*1.0
    plt.text(c/2, yMin-yDelta, "c/2")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('a=%.2f, b=%.2f, c=%.2f'%(a, b, c))
    plt.legend(scatterpoints=1)
    plt.xlim([xMin, xMax])
    plt.ylim([yMin, yMax])
    plt.savefig(figFilename)
    plt.show()

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
