
import numpy as np
import matplotlib.pyplot as plt
import pdb

class AndronovHopfNormalFormCalculator:
    def computeRadialNormalForm(self, w,
                                 Fv, Fvv, Fvvv, Fvn, Fvnn, Fvvn, Fn, Fnn, Fnnn,
                                 Gv, Gvv, Gvvv, Gvn, Gvnn, Gvvn, Gn, Gnn, Gnnn):
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
        return({"a":a, "d":d})

    def computeNormalForm(self, getJacobianFunc, 
                                d2F1dX12At000, d2F1dX1dX2At000, d2F1dX22At000,
                                d3F1dX13At000, d3F1dX12dX2At000,
                                d3F1dX1dX22At000, d3F1dX23At000, 
                                d2F2dX12At000, d2F2dX1dX2At000, d2F2dX22At000,
                                d3F2dX13At000, d3F2dX12dX2At000,
                                d3F2dX1dX22At000, d3F2dX23At000, alpha):
        def d2FidX12At000(i):
            if i==1:
                return(d2F1dX12At000)
            elif i==2:
                return(d2F2dX12At000)
            raise ValueError("1<=i<=2")

        def d2FidX1dX2At000(i):
            if i==1:
                return(d2F1dX1dX2At000)
            elif i==2:
                return(d2F2dX1dX2At000)
            raise ValueError("1<=i<=2")

        def d2FidX22At000(i):
            if i==1:
                return(d2F1dX22At000)
            elif i==2:
                return(d2F2dX22At000)
            raise ValueError("1<=i<=2")

        def d3FidX13At000(i):
            if i==1:
                return(d3F1dX13At000)
            elif i==2:
                return(d3F2dX13At000)
            raise ValueError("1<=i<=2")

        def d3FidX12dX2At000(i):
            if i==1:
                return(d3F1dX12dX2At000)
            elif i==2:
                return(d3F2dX12dX2At000)
            raise ValueError("1<=i<=2")

        def d3FidX1dX22At000(i):
            if i==1:
                return(d3F1dX1dX22At000)
            elif i==2:
                return(d3F2dX1dX22At000)
            raise ValueError("1<=i<=2")

        def d3FidX23At000(i):
            if i==1:
                return(d3F1dX23At000)
            elif i==2:
                return(d3F2dX23At000)
            raise ValueError("1<=i<=2")

        def B(i, x, y):
            answer = d2FidX12At000(i)*x[0]*y[0] + \
                     d2FidX1dX2At000(i)*(x[0]*y[1] + x[1]*y[0]) +\
                     d2FidX22At000(i)*x[1]*y[1]
            return(answer)
        def C(i, x, y, u):
            answer = d3FidX13At000(i)*x[0]*y[0]*u[0] + \
                     d3FidX1dX22At000(i)*(x[0]*y[1]*u[1] + x[1]*y[0]*u[1] + \
                                          x[1]*y[1]*u[0]) +\
                     d3FidX12dX2At000(i)*(x[0]*y[0]*u[1] + x[0]*y[1]*u[0] + \
                                          x[1]*y[0]*u[0]) +\
                     d3FidX23At000(i)*x[1]*y[1]*u[1]
            return(answer)

        alphaTildes = np.arange(-10.0, 10.0, 1)
        indexZeroAlphaTilde = np.argmin(np.abs(alphaTildes))
        lambdas = np.empty([alphaTildes.size,2], dtype=complex)
        for i in xrange(len(alphaTildes)):
            jacobian = getJacobianFunc(alpha=alphaTildes[i])
            eigRes = np.linalg.eig(a=jacobian)
            lambdas[i,:] = eigRes[0]
            if i==indexZeroAlphaTilde:
                eigenvectorsAtZero = eigRes[1]
        if lambdas[indexZeroAlphaTilde,0].imag>0:
            indexLambda = 0
        else:
            indexLambda = 1
        qUnNormalized = eigenvectorsAtZero[:,indexLambda]
        pUnNormalized = \
         self._getOrthogonalVector(v=eigenvectorsAtZero[:,1-indexLambda])
        p = pUnNormalized/pUnNormalized[1]
        pConj = np.conjugate(p)
        qNormalizationFactor = np.dot(np.conjugate(p), qUnNormalized)
        q = qUnNormalized/qNormalizationFactor
        qConj = np.conjugate(q)
        omega0 = lambdas[indexZeroAlphaTilde,indexLambda].imag*\
                  qNormalizationFactor

        # print("A q=")
        # print(jacobian.dot(q))
        # print("lambda q=")
        # print(lambdas[indexZeroAlphaTilde,indexLambda]*q)
        # print("t(A) p")
        # print(np.transpose(jacobian).dot(p))
        # print("conjugate(lambda) p")
        # print(lambdas[indexZeroAlphaTilde,indexLambda].conjugate()*p)

        # plt.plot(alphaTildes, lambdas[:,indexLambda].real)
        # plt.xlabel(r'$\alpha$')
        # plt.ylabel(r'u($\alpha$)')
        # plt.axhline(y=0, color="gray")
        # plt.axvline(x=0, color="gray")
        # plt.show()

        indexAlpha = np.argmin(np.abs(alphaTildes-alpha))
        beta = lambdas[indexAlpha,indexLambda].real/\
                lambdas[indexAlpha,indexLambda].imag
        g20 = np.dot(pConj, np.array([B(1, q, q), B(2, q, q)]))
        g11 = np.dot(pConj, np.array([B(1, q, qConj), B(2, q, qConj)]))
        g21 = np.dot(pConj, np.array([C(1, q, q, qConj), C(2, q, q, qConj)]))
        l10 = (1j*g20*g11+omega0*g21).real/(2*omega0)
        print("l1(0)=%f"%(l10))
        if l10>0:
            s = 1
        elif l10<0:
            s = -1
        else:
            raise ValueError("l1(0)==0")
        
        return(np.array([beta, s]))

    def computePoincareNormalForm(self, getJacobianFunc, 
                                   d2F1dX12At000, d2F1dX1dX2At000, 
                                   d2F1dX22At000,
                                   d3F1dX13At000, d3F1dX12dX2At000,
                                   d3F1dX1dX22At000, d3F1dX23At000, 
                                   d2F2dX12At000, d2F2dX1dX2At000, 
                                   d2F2dX22At000,
                                   d3F2dX13At000, d3F2dX12dX2At000,
                                   d3F2dX1dX22At000, d3F2dX23At000):
        def d2FidX12At000(i):
            if i==1:
                return(d2F1dX12At000)
            elif i==2:
                return(d2F2dX12At000)
            raise ValueError("1<=i<=2")

        def d2FidX1dX2At000(i):
            if i==1:
                return(d2F1dX1dX2At000)
            elif i==2:
                return(d2F2dX1dX2At000)
            raise ValueError("1<=i<=2")

        def d2FidX22At000(i):
            if i==1:
                return(d2F1dX22At000)
            elif i==2:
                return(d2F2dX22At000)
            raise ValueError("1<=i<=2")

        def d3FidX13At000(i):
            if i==1:
                return(d3F1dX13At000)
            elif i==2:
                return(d3F2dX13At000)
            raise ValueError("1<=i<=2")

        def d3FidX12dX2At000(i):
            if i==1:
                return(d3F1dX12dX2At000)
            elif i==2:
                return(d3F2dX12dX2At000)
            raise ValueError("1<=i<=2")

        def d3FidX1dX22At000(i):
            if i==1:
                return(d3F1dX1dX22At000)
            elif i==2:
                return(d3F2dX1dX22At000)
            raise ValueError("1<=i<=2")

        def d3FidX23At000(i):
            if i==1:
                return(d3F1dX23At000)
            elif i==2:
                return(d3F2dX23At000)
            raise ValueError("1<=i<=2")

        def B(i, x, y):
            answer = d2FidX12At000(i)*x[0]*y[0] + \
                     d2FidX1dX2At000(i)*(x[0]*y[1] + x[1]*y[0]) +\
                     d2FidX22At000(i)*x[1]*y[1]
            return(answer)
        def C(i, x, y, u):
            answer = d3FidX13At000(i)*x[0]*y[0]*u[0] + \
                     d3FidX1dX22At000(i)*(x[0]*y[1]*u[1] + x[1]*y[0]*u[1] + \
                                          x[1]*y[1]*u[0]) +\
                     d3FidX12dX2At000(i)*(x[0]*y[0]*u[1] + x[0]*y[1]*u[0] + \
                                          x[1]*y[0]*u[0]) +\
                     d3FidX23At000(i)*x[1]*y[1]*u[1]
            return(answer)

        alphaTildes = np.arange(-10.0, 10.0, 1)
        indexZeroAlphaTilde = np.argmin(np.abs(alphaTildes))
        lambdas = np.empty([alphaTildes.size,2], dtype=complex)
        for i in xrange(len(alphaTildes)):
            jacobian = getJacobianFunc(alpha=alphaTildes[i])
            eigRes = np.linalg.eig(a=jacobian)
            lambdas[i,:] = eigRes[0]
            if i==indexZeroAlphaTilde:
                eigenvectorsAtZero = eigRes[1]
        if lambdas[indexZeroAlphaTilde,0].imag>0:
            indexLambda = 0
        else:
            indexLambda = 1
        q = eigenvectorsAtZero[:,indexLambda]
        qConj = np.conjugate(q)
        unNormalizedP = \
         self._getOrthogonalVector(v=qConj)
        p = unNormalizedP/np.dot(np.conjugate(unNormalizedP), q)
        pConj = np.conjugate(p)
        omega0 = lambdas[indexZeroAlphaTilde, indexLambda].imag

        # print("A q=")
        # print(jacobian.dot(q))
        # print("lambda q=")
        # print(lambdas[indexZeroAlphaTilde,indexLambda]*q)
        # print("t(A) p")
        # print(np.transpose(jacobian).dot(p))
        # print("conjugate(lambda) p")
        # print(lambdas[indexZeroAlphaTilde,indexLambda].conjugate()*p)

        # plt.plot(alphaTildes, lambdas[:,indexLambda].real)
        # plt.xlabel(r'$\alpha$')
        # plt.ylabel(r'u($\alpha$)')
        # plt.axhline(y=0, color="gray")
        # plt.axvline(x=0, color="gray")
        # plt.show()

        l = lambdas[indexZeroAlphaTilde,indexLambda]
        lConj = l.conjugate()
        g20 = np.dot(pConj, np.array([B(1, q, q), B(2, q, q)]))
        g11 = np.dot(pConj, np.array([B(1, q, qConj), B(2, q, qConj)]))
        g02 = np.dot(pConj, np.array([B(1, qConj, qConj), B(2, qConj, qConj)]))
        g21 = np.dot(pConj, np.array([C(1, q, q, qConj), C(2, q, q, qConj)]))
        c1 = 1j/(2*omega0)*(g20*g11-2*g11*g11.conjugate()-\
                            g02*g02.conjugate()/3)+g21/2
        # c1 = g20*g11*(2*l+lConj)/(2*l*lConj)+g11*g11.conjugate()/l+\
        #      g02*g02.conjugate()/(2*(2*l-lConj))+g21/2.0
        # pdb.set_trace()
        return(np.array([l, c1]))

    def _getOrthogonalVector(self, v):
        if v[0].real!=0 or v[0].imag!=0:
            vOrthogonal = np.array([(-v[1]/v[0]).conjugate(), 1.0])
            return(vOrthogonal)
        raise ValueError('Argument must be different from zero')
