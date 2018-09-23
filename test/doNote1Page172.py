
import sys
import pdb
import numpy as np
from INapIKModel import INapIKModel
from INapIKExamplePage172ConstantsStore import INapIKExamplePage172ConstantsStore

def main(argv):
    vAH = INapIKExamplePage172ConstantsStore.vAH
    iAH = INapIKExamplePage172ConstantsStore.iAH

    i = lambda t: iAH
    model = INapIKModel.getLowThresholdInstance(i=i)
    nAH = model._nInf(v=vAH)
    eK = model._eK
    eNa = model._eNa
    gL = model._gL
    gK = model._gK
    gNa = model._gNa
    mK = model._mK
    nK = model._nK
    c = model._c
    tau = model._tau(0.0)
    mInf = model._mInf
    nInf = model._nInf

    dMInf = lambda v: mInf(v=v)/mK*(1-mInf(v=v))
    d2MInf = lambda v: dMInf(v=v)/mK*(1-2*mInf(v=v))
    d3MInf = lambda v: d2MInf(v=v)/mK*(1-2*mInf(v=v))-\
                        2*dMInf(v=v)**2/mK
    dF = (-gL-gNa*(dMInf(v=vAH)*(vAH-eNa)+mInf(v=vAH))-gK*nAH)/c
    d2F = -gNa/c*(d2MInf(v=vAH)*(vAH-eNa)+2*dMInf(v=vAH))
    d3F = -gNa/c*(d3MInf(v=vAH)*(vAH-eNa)+3*d2MInf(v=vAH))

    dNInf = lambda v: nInf(v=v)/nK*(1-nInf(v=v))
    d2NInf = lambda v: dNInf(v=v)/nK*(1-2*nInf(v=v))
    d3NInf = lambda v: d2NInf(v=v)/nK*(1-2*nInf(v=v))-\
                        2*dNInf(v=v)**2/nK
    dG = dNInf(v=vAH)
    d2G = d2NInf(v=vAH)
    d3G = d3NInf(v=vAH)

    beta = gK/c
    k0 = vAH-eK
    mu = 1.0/tau

    w2 = np.linalg.det(model.getJacobian(v0=vAH, n0=nAH))
    w = np.sqrt(w2)

    fxx = d2F-2*mu/k0
    fxy = -w/k0
    fxxy = 0.0
    fxxx = d3F
    fxyy = 0.0
    fyy = 0.0
    fyyy = 0.0
    gyy = 0.0
    gxy = mu/k0
    gxx = mu/w*(beta*k0*d2G-d2F+2*mu/k0)
    gxxx = mu/w*(beta*k0*d3G-d3F)
    gyyy = 0.0
    gxyy = 0.0
    gxxy = 0.0
    

    '''
    a = (d3F+mu/k0**2-
          (d2F-mu/k0)*(1.0/k0+mu/w2*(beta*k0*d2G-d2F+2*mu/k0)))/16.0
    d = (((-2*w/k0-mu/w*(beta*k0*d2G-d2F+2*mu/k0))*
          mu/w*(beta*k0*d2G-d2F+2*mu/k0)-
          (-2*mu/k0-(d2F-2*mu/k0))*(d2F-2*mu/k0)-
          2*((mu/w*(beta*k0*d2G-d2F+2*mu/k0))**2+(d2F-2*mu/k0)**2)-
          ((mu/w*(beta*k0*d2G-d2F+2*mu/k0)-2*w/k0)**2+
           (-(d2F-2*mu/k0)+2*mu/k0)**2)/3.0)/(2*w)+
         mu/w*(beta*k0*d3G-d3F))/16.0
    d = (((-2-5*mu**2/w**2)*(d2F-2*mu/k0)**2+
          (2*mu/k0+10*mu**2/w**2*beta*k0*d2G)*(d2F-2*mu/k0)-
          5*mu**2/w**2*(beta*k0*d2G)**2-beta*mu*d2G-
          2*(w**2+mu**2)/k0**2)/(3*w)+
         mu/w*(beta*k0*d3G-d3F))/16.0
    '''

    a = ((gyy*fyy-gxx*fxx+fxy*(fxx+fyy)-gxy*(gxx+gyy))/w+
         (fxxx+gxxy+fxyy+gyyy))/16.0
    d = ((-2*(gyy**2+fxx**2)+
           (fxy*gxx+gxy*fyy)+
           5*(fxy*gyy+gxy*fxx)-
           5*(gxx**2+fyy**2)-
           5*(gxx*gyy+fxx*fyy)-
           2*(fxy**2+gxy**2))/(3*w)+
         (gxxx+gxyy-fxxy-fyyy))/16.0

    print('a=%f, d=%f'%(a,d))

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

