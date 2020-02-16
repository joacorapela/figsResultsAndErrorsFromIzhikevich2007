
import sys
import numpy as np
import pdb

def main(argv):
    i0 = 3.0
    v0 = -55.0
#     v0 = -57.0
#     v0 = -75.0
    t0 = 0.0
    tf = 6.5
    dt = 1e-5
    v_sn = -60.9325
    i_sn = 4.51
    a = .1887
    c = 1
    singularityMargin = .05
    resultsFilename = 'results/analyticalSolutionNormalFormExampleP163b_i0%.02fv0%.02f.npz'%(i0,v0)

    def getConstantForV0LargerThr(v0, v_sn, sqrtFactor):
        return(np.arctanh(1/(sqrtFactor*(v0-v_sn))))
    def getConstantForV0SmallerThr(v0, v_sn, sqrtFactor):
        return(np.arctanh(sqrtFactor*(v0-v_sn)))

    times = np.arange(t0, tf, dt);
    k = c*(i0-i_sn)
    sqrtFactor = np.sqrt(abs(a/k))
    v0Thr = np.sqrt(abs(c/a*(i0-i_sn)));
    if abs(v0-v_sn)<v0Thr:
        constant = getConstantForV0SmallerThr(v0=v0, 
                                               v_sn=v_sn, 
                                               sqrtFactor=sqrtFactor)
        vs = v_sn+1/sqrtFactor*np.tanh(k*sqrtFactor*times+constant)
    elif abs(v0-v_sn)>v0Thr:
        constant = getConstantForV0LargerThr(v0=v0, 
                                              v_sn=v_sn, 
                                              sqrtFactor=sqrtFactor)
        singularTime = -constant/(k*sqrtFactor)
        times = times[(times<(singularTime-singularityMargin))|((singularTime+singularityMargin)<times)]
        vs = v_sn+1/sqrtFactor*1/np.tanh(k*sqrtFactor*times+constant)
    else:
        vs = v0*np.ones(len(times))
    np.savez(resultsFilename, times=times, vs=vs)

if __name__ == '__main__':
    main(sys.argv)

