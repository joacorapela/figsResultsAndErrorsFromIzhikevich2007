
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

    w2 = np.linalg.det(model.getJacobian(v0=vAH, n0=nAH))
    w = np.sqrt(w2)

    dMInf = lambda v: mInf(v=v)/mK*(1-mInf(v=v))
    d2MInf = lambda v: dMInf(v=v)/mK*(1-2*mInf(v=v))
    d3MInf = lambda v: d2MInf(v=v)/mK*(1-2*mInf(v=v))-\
                        2*dMInf(v=v)**2/mK
    Fv = (-gL-gNa*(dMInf(v=vAH)*(vAH-eNa)+mInf(v=vAH))-gK*nAH)/c
    Fvv = -gNa/c*(d2MInf(v=vAH)*(vAH-eNa)+2*dMInf(v=vAH))
    Fvvv = -gNa/c*(d3MInf(v=vAH)*(vAH-eNa)+3*d2MInf(v=vAH))
    Fvn = -gK/c
    Fvnn = 0.0
    Fvvn = 0.0
    
    Fn = -gK/c*(vAH-eK)
    Fnn = 0.0
    Fnnn = 0.0

    dNInf = lambda v: nInf(v=v)/nK*(1-nInf(v=v))
    d2NInf = lambda v: dNInf(v=v)/nK*(1-2*nInf(v=v))
    d3NInf = lambda v: d2NInf(v=v)/nK*(1-2*nInf(v=v))-\
                        2*dNInf(v=v)**2/nK
    Gv = dNInf(v=vAH)/tau
    Gvv = d2NInf(v=vAH)/tau
    Gvvv = d3NInf(v=vAH)/tau
    Gvn = 0.0
    Gvnn = 0.0
    Gvvn = 0.0
    Gn = -1.00/tau
    Gnn = 0.0
    Gnnn = 0.0

    fxx = Fvv+Fvn*(-Fv/Fn)+(Fvn+Fnn*(-Fv/Fn))*(-Fv/Fn)
    fxy = Fvn*(-w/Fn)+Fnn*(-w/Fn)*(-Fv/Fn)
    fxxx = Fvvv+Fvvn*(-Fv/Fn)+(Fvvn+Fvnn*(-Fv/Fn))*(-Fv/Fn)+\
           ((Fvvn+Fvnn*(-Fv/Fn))+(Fvnn+Fnnn*(-Fv/Fn))*(-Fv/Fn))*(-Fv/Fn)
    fxxy = Fvvn*(-w/Fn)+2*Fvnn*(-Fv/Fn)*(-w/Fn)+Fnnn*(-Fv/Fn)**2*(-w/Fn)

    fyy = Fnn*(-w/Fn)**2
    fyyy = Fnnn*(-w/Fn)**3
    fxyy = (Fvnn+Fnnn*(-Fv/Fn))*(-w/Fn)**2

    gxx = (Fv*(Fvv+2*Fvn*(-Fv/Fn)+Fnn*(-Fv/Fn)**2)+
           Fn*(Gvv+2*Gvn*(-Fv/Fn)+Gnn*(-Fv/Fn)**2))/(-w)
    gxy = (Fv*(Fvn*(-w/Fn)+Fnn*(-w/Fn)*(-Fv/Fn))+
           Fn*(Gvn*(-w/Fn)+Gnn*(-w/Fn)*(-Fv/Fn)))/(-w)
    gxxx = (Fv*(Fvvv+Fvvn*(-Fv/Fn)+2*(Fvvn+Fvnn*(-Fv/Fn))*(-Fv/Fn)+
                 (Fvnn+Fnnn*(-Fv/Fn))*(-Fv/Fn)**2)+
            Fn*(Gvvv+Gvvn*(-Fv/Fn)+2*(Gvvn+Gvnn*(-Fv/Fn))*(-Fv/Fn)+
                 (Gvnn+Gnnn*(-Fv/Fn))*(-Fv/Fn)**2))/(-w)
    gxxy = (Fv*(Fvvn*(-w/Fn)+2*Fvnn*(-w/Fn)*(-Fv/Fn)+
                 Fnnn*(-w/Fn)*(-Fv/Fn)**2)+
            Fn*(Gvvn*(-w/Fn)+2*Gvnn*(-w/Fn)*(-Fv/Fn)+
                 Gnnn*(-w/Fn)*(-Fv/Fn)**2))/(-w)

    gyy = (Fv*Fnn*(-w/Fn)**2+Fn*Gnn*(-w/Fn)**2)/(-w)
    gyyy = (Fv*Fnnn*(-w/Fn)**3+Fn*Gnnn*(-w/Fn)**3)/(-w)
    gxyy = (Fv*(Fvnn+Fnnn*(-Fv/Fn))*(-w/Fn)**2+
            Fn*(Gvnn+Gnnn*(-Fv/Fn))*(-w/Fn)**2)/(-w)

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

