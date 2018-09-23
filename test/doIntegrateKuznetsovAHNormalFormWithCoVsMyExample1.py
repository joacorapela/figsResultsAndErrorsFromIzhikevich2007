
import sys
import numpy as np
from scipy.integrate import ode
from KuznetsovAHNormalFormWithCoVs import KuznetsovAHNormalFormWithCoVs
from KuznetsovAHNormalFormMyExample1 import h, hInv, hJacobian

def main(argv):
    if len(argv)!=5:
        sys.exit("Usage: %s beta0 sign x10 x20"%argv[0])
    beta = float(argv[1])
    sign = float(argv[2])
    x10 = float(argv[3])
    x20 = float(argv[4])
    t0 = 0.0
    tf = 200.0
    dt = 1e-3
    resultsFilename = \
     'results/integrationKuznetsovAHNormalFormWithCoVsMyExample1Beta%.02fSign%dX10%.02fX20%.02f.npz'%(beta,sign,x10,x20)

    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    kAHNormalFormWithCoVs = KuznetsovAHNormalFormWithCoVs(beta=beta, 
                                                           sign=sign,
                                                           hJacobian=hJacobian,
                                                           hInv=hInv)
    integrator = ode(kAHNormalFormWithCoVs.deriv).set_integrator('vode', 
                                                                 max_step=dt)

    y0 = h(np.array([x10, x20]))
    integrator.set_initial_value(y0, t0)
    ys = np.empty((2, nTSteps+1))
    ys[:, 0] = y0

    t = t0
    step = 0
    successfulIntegration = True
    while successfulIntegration and step<nTSteps:
        step = step+1
        if step%100000==0:
            print('Processing time %.05f out of %.02f' % (t, tf))
            sys.stdout.flush()
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        times[step] = t
        ys[:, step] = y

    np.savez(resultsFilename, x10=x10, x20=x20, times=times, ys=ys)

if __name__ == '__main__':
    main(sys.argv)

