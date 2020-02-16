
import sys
import pdb
import math
import matplotlib.pyplot as plt
from plotFunctions import plotVectorField

def main(argv):
    a = -1.0
    b = 1.0
    c = 2.0
    colorSaddle = (1.0, 0.0, 0.0)
    colorStableNode = (0.0, 1.0, 0.0)
    colorStableFocus = (0.0, 0.5, 0.0)
    colorUnstableNode = (0.0, 0.0, 1.0)
    colorUnstableFocus = (0.0, 0.0, 0.5)
    xMin = -2.0
    xMax = 2.0
    nXs = 16 
    yMin = -2.0
    yMax = 8.0
    nYs=16
    

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
    if a>(2*b-c**2)/4:
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
    plotVectorField(xDotFun=f, yDotFun=g, 
                               xMin=xMin, xMax=xMax, nXs=nXs,
                               yMin=yMin, yMax=yMax, nYs=nYs)
    plt.scatter(xe1, ye1, marker="o", label=e1Type, color=e1Color)
    plt.scatter(xe2, ye2, marker="o", label=e2Type, color=e2Color)
    plt.legend(scatterpoints=1)
    plt.show()

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
