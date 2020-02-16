
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def yDot(y0, t):
    return(-1+y(y0=y0, t=t)**2)

def y(y0, t):
    if abs(y0)<1:
        return(yAbsY0Less1(y0=y0, t=t))
    elif abs(y0)>1:
        return(yAbsY0Greater1(y0=y0, t=t))
    else:
        return(1.0)

def yAbsY0Less1(y0, t):
    c = np.arctanh(y0)
    answer = np.tanh(-t+c)
    return(answer)

def yAbsY0Greater1(y0, t):
    c = np.arctanh(1/y0)
    answer = 1.0/np.tanh(-t+c)
    return(answer)

def buildYDostGrid(ts, y0s):
    yDotsGrid = np.empty((len(y0s), len(ts)))
    for i in xrange(len(y0s)):
        y0 = y0s[i]
        for j in xrange(len(ts)):
            t = ts[j]
            yDotsGrid[i,j] = yDot(y0=y0, t=t)
    return(yDotsGrid)

def main(argv):
    if len(argv)!=7:
        print('Usage %s y0Min y0Max dy0 tf dt maxAbsYDot'%argv[0])
        return
    t0 = 0
    y0Min = float(argv[1])
    y0Max = float(argv[2])
    dY0 = float(argv[3])
    tf = float(argv[4])
    dt = float(argv[5])
    maxAbsYDot = float(argv[6])

    ts = np.arange(t0, tf, dt)
    y0s = np.arange(y0Min, y0Max, dY0)
    tsGrid, y0sGrid = np.meshgrid(ts, y0s)
    yDotsGrid = buildYDostGrid(ts=ts, y0s=y0s)
    tDotsGrid = np.ones(yDotsGrid.shape)

    yDotsGrid[np.where(np.abs(yDotsGrid)>maxAbsYDot)] = maxAbsYDot

    plt.quiver(tsGrid, y0sGrid, tDotsGrid, yDotsGrid)
    plt.axhline(y=1, color="red")
    plt.axhline(y=-1, color="blue")
    plt.xlabel("Time (sec)")
    plt.ylabel("y(t)")
    plt.show()

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
