
import numpy as np
import pdb

class QuadraticIFModel:

    def __init__(self, i, iSN, c, vSN, a, vReset, vMax):
        # alpha = sqrt(c/a*(i-iSN))
        # beta = sqrt(c*a*(i-iSN))
        self._i = i
        self._iSN = iSN
        self._c = c
        self._vSN = vSN
        self._a = a
        self._vReset = vReset
        self._vMax = vMax
        self._alpha = np.sqrt(c/a*(i-iSN))
        self._beta = np.sqrt(c*a*(i-iSN))
        self._thetaReset = np.arctan((vReset-vSN)/self._beta)
        self._thetaMax = np.arctan((vMax-vSN)/self._beta)

    def getSolution(self, v0, t0, tf, srate):
        initialSegmentTs, initialSegmentVs = \
         self._getSolutionInitialSegment(v0=v0, t0=t0, tf=tf, srate=srate)
        initialSegmentTF = initialSegmentTs[-1]
        fullSegmentDuration = (self._thetaMax-self._thetaReset)/\
                               np.sqrt(self._a*self._c*(self._i-self._iSN))
        nFullSegments = np.floor((tf-initialSegmentTF)/fullSegmentDuration)
        finalSegmentDuration = tf-(initialSegmentTF+
                                    nFullSegments*fullSegmentDuration)
        fullSegmentVs = self._getSolutionFullSegment(srate=srate)
        finalSegmentVs = fullSegmentVs[0:(finalSegmentDuration*srate)]
        vs = np.concatenate((initialSegmentVs, 
                             np.tile(A=fullSegmentVs, reps=nFullSegments),
                             finalSegmentVs))
        times = np.arange(t0, tf+1.0/srate, 1.0/srate)
        return(times, vs)

    def _v(self, t, c0):
        answer = self._vSN+np.sqrt(self._c/self._a*(self._i-self._iSN))*\
                           np.tan(np.sqrt(self._a*self._c*
                                           (self._i-self._iSN))*t+c0)
        return(answer)

    def _getSolutionInitialSegment(self, v0, t0, tf, srate):
        c0 = np.arctan((v0-self._vSN)/np.sqrt(self._c/self._a*
                                               (self._i-self._iSN)))-\
              np.sqrt(self._a*self._c*(self._i-self._iSN))*t0
        segmentTF = min(tf, (self._thetaMax-c0)/\
                            np.sqrt(self._a*self._c*(self._i-self._iSN)))
        ts = np.arange(t0, segmentTF, 1.0/srate)
        vs = self._v(t=ts, c0=c0)
        return(ts, vs)

    def _getSolutionFullSegment(self, srate):
        segmentTF = (self._thetaMax-self._thetaReset)/\
                     np.sqrt(self._a*self._c*(self._i-self._iSN))
        ts = np.arange(0, segmentTF, 1.0/srate)
        vs = self._v(t=ts, c0=self._thetaReset)
        return(vs)
