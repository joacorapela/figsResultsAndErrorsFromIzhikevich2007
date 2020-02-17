
import sys
import pdb
import numpy as np
from INapIKModel import INapIKModel
from INapIKExamplePage172ConstantsStore import INapIKExamplePage172ConstantsStore
from AndronovHopfNormalFormCalculator import AndronovHopfNormalFormCalculator

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

    ahNormalFormCalculator = AndronovHopfNormalFormCalculator()
    res = ahNormalFormCalculator.computeRadialNormalForm(w=w, Fv=Fv, 
                                                              Fvv=Fvv,
                                                              Fvvv=Fvvv, 
                                                              Fvn=Fvn, 
                                                              Fvnn=Fvnn, 
                                                              Fvvn=Fvvn, 
                                                              Fn=Fn, Fnn=Fnn,
                                                              Fnnn=Fnnn,
                                                              Gv=Gv, 
                                                              Gvv=Gvv,
                                                              Gvvv=Gvvv,
                                                              Gvn=Gvn,
                                                              Gvnn=Gvnn,
                                                              Gvvn=Gvvn,
                                                              Gn=Gn, 
                                                              Gnn=Gnn,
                                                              Gnnn=Gnnn)
    print('a=%f, d=%f'%(res["a"],res["d"]))

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

