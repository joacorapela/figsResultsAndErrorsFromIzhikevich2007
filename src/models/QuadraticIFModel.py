
import numpy as np
import pdb

class QuadraticIFModel:

    def __init__(self, i, iSN, c, vSN, a, vReset, vMax, spikeDuration):
        self._i = i
        self._iSN = iSN
        self._c = c
        self._vSN = vSN
        self._a = a
        self._vReset = vReset
        self._vMax = vMax
        self._spikeDuration = spikeDuration
        self._beta = np.sqrt(c/a*(i-iSN))
        self._alpha = np.sqrt(c*a*(i-iSN))
        self._thetaReset = np.arctan((vReset-vSN)/self._beta)
        self._thetaMax = np.arctan((vMax-vSN)/self._beta)

    def getSolution(self, v0, t0, tf, srate):
        dt = 1.0/srate
        c0Initial, tfInitial = self._getConstantsInitialSegment(v0=v0, t0=t0,
                                                                       dt=dt)
        if tf>tfInitial:
            tsInitial = np.arange(t0, tfInitial, dt)
            vsInitial = \
             np.concatenate((self._v(t=tsInitial, c0=c0Initial), 
                              np.tile(A=self._vMax, 
                                       reps=round(self._spikeDuration*srate))))
            c0Full, relativeTFFull = self._getConstantsFullSegment(dt=dt)
            nFullSegments = np.floor((tf-(tfInitial+self._spikeDuration))/
                                     (relativeTFFull+self._spikeDuration))
            relativeTFFinal = tf - (tfInitial+self._spikeDuration+
                                     nFullSegments*
                                     (relativeTFFull+self._spikeDuration))
            relativeTsFull = np.arange(0, relativeTFFull, dt)
            vsOneFullSegment = \
             np.concatenate((self._v(t=relativeTsFull, c0=c0Full),
                                np.tile(A=self._vMax, 
                                         reps=np.round(self._spikeDuration*
                                                        srate))))
            relativeTsFinal = np.arange(0, relativeTFFinal, dt)
            if relativeTFFinal<relativeTFFull:
                vsFinal = self._v(t=relativeTsFinal, c0=c0Full)
            else:
                vsFinal = \
                 np.concatenate(((self._v(t=relativeTsFull, c0=c0Full),
                                   np.tile(A=self._vMax, 
                                            reps=np.round((relativeTFFinal-
                                                           relativeTFFull)*
                                                          srate)))))
            vs = np.concatenate((vsInitial, 
                                  np.tile(A=vsOneFullSegment, 
                                           reps=nFullSegments), 
                                  vsFinal))
            ts = t0+np.arange(0, len(vs)*dt, dt)
        else:
            ts = np.arange(t0, tf, dt)
            vs = self._v(t=ts, c0=c0Initial)
        return(ts, vs)

    def _v(self, t, c0):
        answer = self._vSN+np.sqrt(self._c/self._a*(self._i-self._iSN))*\
                           np.tan(np.sqrt(self._a*self._c*
                                           (self._i-self._iSN))*t+c0)
        return(answer)

    def _getConstantsInitialSegment(self, v0, t0, dt):
        c0 = np.arctan((v0-self._vSN)/self._beta)-self._alpha*t0
        segmentTF = (self._thetaMax-c0)/self._alpha
        segmentTF = round(segmentTF/dt)*dt
        return(c0, segmentTF)

    def _getConstantsFullSegment(self, dt):
        c0 = self._thetaReset
        segmentTF = (self._thetaMax-self._thetaReset)/self._alpha
        segmentTF = round(segmentTF/dt)*dt
        return(c0, segmentTF)
