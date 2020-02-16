
import numpy as np
import pdb
import matplotlib.pyplot as plt

def plotLowThresholdINapIKVectorField(i=0.0, c=1.0, eL=-78, gL=8, gNa=20, 
                                       gK=10,
                                       mVOneHalf=-20, mK=15, 
                                       nVOneHalf=-45, nK=5, tauV=1, eNa=60,
                                       eK=-90, nDotScaleFactor=200, 
                                       vMin=-90.0, vMax=20.0, 
                                       nVs=19, nVsDense=100,
                                       nMin=0.0, nMax=0.7, nNs=18, 
                                       vNullclineLabel="v nullcline",
                                       nNullclineLabel="n nullcline",
                                       ylim=None):
    plotINapIKVectorField(i=i, c=c, eL=eL, gL=gL, 
                               eNa=eNa, gNa=gNa, eK=eK, gK=gK,
                               mVOneHalf=mVOneHalf, mK=mK,
                               nVOneHalf=nVOneHalf, nK=nK, 
                               tauV=tauV,
                               nDotScaleFactor=nDotScaleFactor, 
                               vMin=vMin, vMax=vMax, nVs=nVs, 
                               nVsDense=nVsDense, nMin=nMin, nMax=nMax, nNs=nNs,
                               vNullclineLabel=vNullclineLabel,
                               nNullclineLabel=nNullclineLabel, ylim=ylim)

def plotHighThresholdINapIKVectorField(i=0.0, c=1.0, 
                                       eL=-80, gL=8, 
                                       eNa=60, gNa=20, 
                                       eK=-90, gK=10,
                                       mVOneHalf=-20, mK=15, 
                                       nVOneHalf=-25, nK=5, 
                                       tauV=1, nDotScaleFactor=200, 
                                       vMin=-90.0, vMax=20.0, 
                                       nVs=19, nVsDense=100, nMin=0.0, nMax=0.7, nNs=18, 
                                       vNullclineLabel="v nullcline",
                                       nNullclineLabel="n nullcline",
                                       ylim=None):
    plotINapIKVectorField(i=i, c=c, eL=eL, gL=gL, 
                               eNa=eNa, gNa=gNa, eK=eK, gK=gK,
                               mVOneHalf=mVOneHalf, mK=mK, 
                               nVOneHalf=nVOneHalf, nK=nK,
                               tauV=tauV, 
                               nDotScaleFactor=nDotScaleFactor, 
                               vMin=vMin, vMax=vMax, nVs=nVs, 
                               nVsDense=nVsDense, nMin=nMin, nMax=nMax, nNs=nNs,
                               vNullclineLabel=vNullclineLabel,
                               nNullclineLabel=nNullclineLabel, ylim=ylim)

def plotINapIKVectorField(i, c, eL, gL, eNa, gNa, eK, gK, 
                             mVOneHalf, mK, nVOneHalf, nK, tauV, 
                             nDotScaleFactor=200, vMin=-90.0, vMax=20.0, 
                             nVs=19, nVsDense=100,
                             nMin=0.0, nMax=0.7, nNs=18, 
                             vNullclineLabel="v nullcline",
                             nNullclineLabel="n nullcline",
                             xlabel="membrange voltage, V (mV)",
                             ylabel=r"$K^+$ activation variable, n",
                             ylim=None):
    if ylim is None:
        ylim = (nMin, nMax)
    vs = np.arange(vMin, vMax, (vMax-vMin)/nVs)
    ns = np.arange(nMin, nMax, (nMax-nMin)/nNs)
    vsGrid, nsGrid = np.meshgrid(vs, ns)
    iLsGrid = gL*(vsGrid-eL)
    mInfGrid = 1.0/(1+np.exp((mVOneHalf-vsGrid)/mK))
    iNapsGrid = gNa*mInfGrid*(vsGrid-eNa)
    nInfGrid = 1.0/(1+np.exp((nVOneHalf-vsGrid)/nK))
    IKsGrid = gK*nsGrid*(vsGrid-eK)
    iTsGrid = iLsGrid+iNapsGrid+IKsGrid
    vDots = (i-iTsGrid)/c
    nDots = (nInfGrid-nsGrid)/tauV 
    vsDense = np.arange(vMin, vMax, (vMax-vMin)/nVsDense)
    iLsDense = gL*(vsDense-eL)
    mInfDense = 1.0/(1+np.exp((mVOneHalf-vsDense)/mK))
    iNapsDense = gNa*mInfDense*(vsDense-eNa)
    nInfDense = 1.0/(1+np.exp((nVOneHalf-vsDense)/nK))
    vNullcline = (i-iLsDense-iNapsDense)/(gK*(vsDense-eK))
    nNullcline = nInfDense

    plt.quiver(vsGrid, nsGrid, vDots, nDotScaleFactor*nDots)
    plotINapIKNullclines(i=i, eL=eL, gL=gL, eNa=eNa, gNa=gNa, eK=eK, gK=gK,
                              mVOneHalf=mVOneHalf, mK=mK, 
                              nVOneHalf=nVOneHalf, nK=nK,
                              nVsDense=nVsDense, vMin=vMin, vMax=vMax,
                              vNullclineLabel=vNullclineLabel,
                              nNullclineLabel=nNullclineLabel)
    plt.legend()
    plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def plotINapIKNullclines(i, eL, gL, eNa, gNa, eK, gK, 
                            mVOneHalf, mK, nVOneHalf, nK, 
                            nVsDense=100, vMin=-90.0, vMax=20.0,
                            vNullclineLabel="v nullcline",
                            nNullclineLabel="n nullcline"):
    vsDense = np.arange(vMin, vMax, (vMax-vMin)/nVsDense)
    iLsDense = gL*(vsDense-eL)
    mInfDense = 1.0/(1+np.exp((mVOneHalf-vsDense)/mK))
    iNapsDense = gNa*mInfDense*(vsDense-eNa)
    nInfDense = 1.0/(1+np.exp((nVOneHalf-vsDense)/nK))
    vNullcline = (i-iLsDense-iNapsDense)/(gK*(vsDense-eK))
    nNullcline = nInfDense

    plt.plot(vsDense, vNullcline, label=vNullclineLabel)
    plt.plot(vsDense, nNullcline, label=nNullclineLabel)

def plotHighThresholdINatVectorField(i=0.0, c=1.0, 
                                            gL=1.0, eL=-70.0,
                                            gNa=10.0, eNa=60.0,
                                                    mVOneHalf=-40.0, mK=15.0,
                                            hVOneHalf=-42.0, hK=-7.0,
                                            tauH=5.0, 
                                            hDotScaleFactor=200, 
                                            vMin=-90.0, vMax=20.0, 
                                            nVs=19, nVsDense=100,
                                            hMin=0.0, hMax=1.0, nHs=18, 
                                            vNullclineLabel="v nullcline",
                                            hNullclineLabel="h nullcline",
                                            ylim=None):
    plotINatVectorField(i=i, c=c, gL=gL, eL=eL, gNa=gNa, eNa=eNa,
                           mVOneHalf=mVOneHalf, mK=mK, hVOneHalf=hVOneHalf, 
                           hK=hK, tauH=tauH,
                           hDotScaleFactor=hDotScaleFactor, nVsDense=nVsDense, 
                           vMin=vMin, vMax=vMax, nVs=nVs,
                           hMin=hMin, hMax=hMax, nHs=nHs, 
                           vNullclineLabel=vNullclineLabel,
                           hNullclineLabel=hNullclineLabel,
                           ylim=ylim)
    plt.gca().invert_yaxis()

def plotLowThresholdINatVectorField(i=0.0, c=1.0, 
                                           gL=1.0, eL=-70.0,
                                           gNa=15.0, eNa=60.0,
                                           mVOneHalf=-40.0, mK=15.0,
                                           hVOneHalf=-62.0, hK=-7.0,
                                           tauH=5.0, 
                                           hDotScaleFactor=200, 
                                           vMin=-90.0, vMax=50.0, 
                                           nVs=19, nVsDense=100,
                                           hMin=0.0, hMax=1.0, nHs=18, 
                                           vNullclineLabel="v nullcline",
                                           hNullclineLabel="h nullcline",
                                           ylim=None):
    plotINatVectorField(i=i, c=c, gL=gL, eL=eL, gNa=gNa, eNa=eNa,
                           mVOneHalf=mVOneHalf, mK=mK, hVOneHalf=hVOneHalf, 
                           hK=hK, tauH=tauH,
                           hDotScaleFactor=hDotScaleFactor, nVsDense=nVsDense, 
                           vMin=vMin, vMax=vMax, nVs=nVs,
                           hMin=hMin, hMax=hMax, nHs=nHs, 
                           vNullclineLabel=vNullclineLabel,
                           hNullclineLabel=hNullclineLabel,
                           ylim=ylim)
    plt.gca().invert_yaxis()

def plotINatVectorField(i, c, gL, eL, gNa, eNa,
                           mVOneHalf, mK, hVOneHalf, hK, tauH,
                           hDotScaleFactor=200, nVsDense=100, 
                           vMin=-90.0, vMax=20.0, nVs=19,
                           hMin=0.0, hMax=0.7, nHs=18, 
                           ylim=None):
    if ylim is None:
        ylim = (hMin, hMax)
    vs = np.arange(vMin, vMax, (vMax-vMin)/nVs)
    hs = np.arange(hMin, hMax, (hMax-hMin)/nHs)
    vsGrid, hsGrid = np.meshgrid(vs, hs)
    iLsGrid = gL*(vsGrid-eL)
    mInfGrid = 1.0/(1+np.exp((mVOneHalf-vsGrid)/mK))
    hInfGrid = 1.0/(1+np.exp((hVOneHalf-hsGrid)/hK))
    iNatGrid = gNa*np.power(mInfGrid,3)*hsGrid*(vsGrid-eNa)
    iTsGrid = iLsGrid+iNatGrid
    vDots = (i-iTsGrid)/c
    hDots = (hInfGrid-hsGrid)/tauH

    plt.quiver(vsGrid, hsGrid, vDots, hDotScaleFactor*hDots)
    plotINatNullclines(i=i, gL=gL, eL=eL, gNa=gNa, eNa=eNa, mK=mK, hK=hK,
                            nVsDense=nVsDense, vMin=vMin, vMax=vMax,
                            vNullclineLabel=vNullclineLabel,
                            hNullclineLabel=hNullclineLabel)
    plt.legend()
    plt.ylim(ylim)

def plotINatNullclines(i=0.0, eL=-70.0, gL=1.0, eNa=60.0, gNa=15.0, 
                              mVOneHalf=-40.0, mK=15.0, 
                              hVOneHalf=-62.0, hK=-7.0,
                              nVsDense=100, vMin=-90.0, vMax=20.0,
                              vNullclineLabel="v nullcline",
                              hNullclineLabel="h nullcline"):
    vsDense = np.arange(vMin, vMax, (vMax-vMin)/nVsDense)
    iLsDense = gL*(vsDense-eL)
    mInfDense = 1.0/(1+np.exp((mVOneHalf-vsDense)/mK))
    hInfDense = 1.0/(1+np.exp((hVOneHalf-vsDense)/hK))
    iNatDense = gNa*np.power(mInfDense,3)*(vsDense-eNa)
    vNullcline = (i-iLsDense)/iNatDense
    hNullcline = hInfDense

    plt.plot(vsDense, vNullcline, label=vNullclineLabel)
    plt.plot(vsDense, hNullcline, label=hNullclineLabel)

def plotStrogatzUnstableLimitCycleVectorField(mu, w, b, xMin, xMax, nXs,
                                                  yMin, yMax, nYs):
    def xDotFun(x, y):
        answer = mu*x+(x**2+y**2)*x*(1-(x**2+y**2))-y*(w+b*(x**2+y**2))
        return(answer)
    def yDotFun(x, y):
        answer = mu*y+(x**2+y**2)*y*(1-(x**2+y**2))+x*(w+b*(x**2+y**2))
        return(answer)
    plotVectorField(xDotFun=xDotFun, yDotFun=yDotFun, 
                                     xMin=xMin, xMax=xMax, nXs=nXs, 
                                     yMin=yMin, yMax=yMax, nYs=nYs)

def plotVectorField(xDotFun, yDotFun, xMin, xMax, nXs, yMin, yMax, nYs):
    xs = np.arange(xMin, xMax, (xMax-xMin)/nXs)
    ys = np.arange(yMin, yMax, (yMax-yMin)/nYs)
    xsGrid, ysGrid = np.meshgrid(xs, ys)

    xDots = np.empty(xsGrid.shape)
    xDots[:] = np.nan
    yDots = np.empty(ysGrid.shape)
    yDots[:] = np.nan
    for i in xrange(xDots.shape[0]):
        for j in xrange(xDots.shape[1]):
            xDots[i,j] = xDotFun(x=xsGrid[i,j], y=ysGrid[i,j])
            yDots[i,j] = yDotFun(x=xsGrid[i,j], y=ysGrid[i,j])
    plt.quiver(xsGrid, ysGrid, xDots, yDots)
