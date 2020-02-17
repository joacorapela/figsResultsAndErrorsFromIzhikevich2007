

class INapIKIntegrator:
    def INapIKIntegrator(self, iNapIKModel):
        _iNapIKModel = iNapIKModel

    def integrate(self, v0, t0, tf, dt):
        integrator = ode(self._iNapIKModel.deriv).set_integrator('vode', max_step=dt)

    y0 = np.array([v0, iNapIKModel._nInf(v=v0)])
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



        fs = np.empty(len(currents))
        for i in currents:
        
