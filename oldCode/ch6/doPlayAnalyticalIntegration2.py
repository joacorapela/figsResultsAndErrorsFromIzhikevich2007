
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):
    if len(argv)!=4:
        print('Usage %s y0 tf dt'%argv[0])
        return
    t0 = 0
    singularMargin = 0.1
    y0 = float(argv[1])
    tf = float(argv[2])
    dt = float(argv[3])


    def getAnalyticalSol(y0, ts):
        if abs(y0)<1:
            return(getAnalyticalSolAbsY0Less1(y0, ts))
        elif abs(y0)>1:
            return(getAnalyticalSolAbsY0Greater1(y0, ts))
        else:
            return(np.ones(len(ts)))

    def getAnalyticalSolAbsY0Less1(y0, ts):
        c = np.arctanh(y0)
        answer = np.tanh(-ts+c)
        return(answer)

    def getAnalyticalSolAbsY0Greater1(y0, ts):
        c = np.arctanh(1/y0)
        answer = 1.0/np.tanh(-ts+c)
        return(answer)

    if abs(y0)<=1:
        ts = np.arange(t0, tf, dt)
        ys = getAnalyticalSol(y0=y0, ts=ts)
    else:
        singularTime = np.arctanh(1/y0)
        if tf>singularTime+singularMargin:
            tsBefore = np.arange(t0, singularTime-singularMargin, dt)
            ysBefore = getAnalyticalSolAbsY0Greater1(y0=y0, ts=tsBefore)
            tsAfter = np.arange(singularTime+singularMargin, tf, dt)
            ysAfter = getAnalyticalSolAbsY0Greater1(y0=y0, ts=tsAfter)
            ts = np.concatenate((tsBefore, tsAfter))
            ys = np.concatenate((ysBefore, ysAfter))
        else:
            ts = np.arange(t0, tf, dt)
            ys = getAnalyticalSolAbsY0Greater1(y0=y0, ts=ts)

    plt.plot(ts, ys, color="black")
    plt.axhline(y=1, color="red")
    plt.axhline(y=-1, color="blue")
    plt.xlabel("Time (sec)")
    plt.ylabel("y(t)")
    plt.show()

    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
