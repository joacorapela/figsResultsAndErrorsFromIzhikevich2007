
import sys
import numpy as np
from scipy.integrate import ode
import pdb
from AndronovHopfNormalForm import AndronovHopfNormalForm
from INapIKExamplePage172ConstantsStore import INapIKExamplePage172ConstantsStore

def main(argv):
    if len(argv)!=4:
        sys.exit("Usage: %s i0 a d"%argv[0])
    i0 = float(argv[1])
    a = float(argv[2])
    d = float(argv[3])
    phi0 = np.pi
    t0 = 0.0
    tf = 200.0
    dt = 1e-3
    resultsFilename = \
     'results/integrationAHNormalFormExampleP172I%.02fa%fd%f.npz'%(i0,a,d)

    def i(t):
        return(i0)
    cb = lambda b: 0.0307*(b-INapIKExamplePage172ConstantsStore.iAH)
    wb = lambda b: 2.1376+0.0407*(b-INapIKExamplePage172ConstantsStore.iAH)
    r0 = np.sqrt(cb(b=i0)/np.abs(a))

    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    ahNormalForm = AndronovHopfNormalForm(b=i, cb=cb, wb=wb, a=a, d=d)
    integrator = ode(ahNormalForm.deriv).set_integrator('vode', max_step=dt)

    y0 = np.array([r0, phi0])
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

