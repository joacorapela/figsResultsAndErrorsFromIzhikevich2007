
import sys
import numpy as np
from scipy.integrate import ode
from INapIKModel import INapIKModel
from INapIKExamplePage172ConstantsStore import INapIKExamplePage172ConstantsStore

def main(argv):
    if len(argv)!=2:
        sys.exit("Usage: %s a"%argv[0])
    a = float(argv[1])
    # i0s = np.arange(15, 20, .25)
    i0s = [14.67]
    vAH = INapIKExamplePage172ConstantsStore.vAH
    n0 = INapIKExamplePage172ConstantsStore.nAH
    t0 = 0.0
    tf = 200.0
    dt = 1e-3
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)

    for i0 in i0s:
        print('Processing i0=%.2f' % (i0))
        cb = 0.03*(i0-INapIKExamplePage172ConstantsStore.iAH)
        r0 = np.sqrt(cb/np.abs(a))
        v0 = vAH-r0
        resultsFilename = 'results/integrationINapIKExampleP172I%.02fa%f.npz'%(i0,a)
        def i(t):
            return(i0)
        iNapIKModel = INapIKModel.getLowThresholdInstance(i=i)
        integrator = ode(iNapIKModel.deriv).set_integrator('vode', max_step=dt)

        y0 = np.array([v0, n0])
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

        np.savez(resultsFilename, i0=i0, times=times, ys=ys)

if __name__ == '__main__':
    main(sys.argv)

