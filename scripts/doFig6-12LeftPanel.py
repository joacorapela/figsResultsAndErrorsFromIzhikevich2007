
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel

def main(argv):
    xticks = np.arange(0, 31, 10)
    iNapIKModel = INapIKModel.getLowThresholdInstance(i=None)
    v0s = np.arange(-62, -53, .001)
    n0s = iNapIKModel._nInf(v=v0s)
    i0s = iNapIKModel.getIInf(v=v0s)

    cs = []
    ws = []
    for i in xrange(len(v0s)):
        v0 = v0s[i]
        n0 = n0s[i]
        jacobian = iNapIKModel.getJacobian(v0=v0, n0=n0)
        eigRes = np.linalg.eig(jacobian)
        cs.append(eigRes[0][0].real)
        ws.append(eigRes[0][0].imag)
    bifurcationIndex = np.argmin(np.abs(cs))
    iAtBifurcation = i0s[bifurcationIndex]
    csDerivAtBifurcation = (cs[bifurcationIndex+1]-cs[bifurcationIndex-1])/\
                           (i0s[bifurcationIndex+1]-i0s[bifurcationIndex-1])
    wsDerivAtBifurcation = (ws[bifurcationIndex+1]-ws[bifurcationIndex-1])/\
                           (i0s[bifurcationIndex+1]-i0s[bifurcationIndex-1])
    wAtBifurcation = ws[bifurcationIndex]
    v0AtBifurcation = v0s[bifurcationIndex]
    n0AtBifurcation = n0s[bifurcationIndex]

    print("iAH=%f"%(iAtBifurcation))
    print("vAH=%f"%(v0AtBifurcation))
    print("nAH=%f"%(n0AtBifurcation))
    print("c(I) deriv at iAH=%f"%(csDerivAtBifurcation))
    print("w(iAH)=%f"%(wAtBifurcation))
    print("w(I) deriv at iAH=%f"%(wsDerivAtBifurcation))

    plt.plot(i0s, cs, label="c(I)", color="blue", linewidth=3,
                  linestyle="dotted")
    plt.plot(i0s, csDerivAtBifurcation*(i0s-iAtBifurcation), 
                  color="blue", linewidth=3, linestyle="solid")
    plt.plot(i0s, ws, label="w(I)", color="red", linewidth=3,
                  linestyle="dotted")
    plt.plot(i0s, wsDerivAtBifurcation*(i0s-iAtBifurcation)+wAtBifurcation, 
                  color="red", linewidth=3, linestyle="solid")
    plt.xticks(xticks)
    plt.text(x=iAtBifurcation, y=-1.0, s="%.04f"%iAtBifurcation)
    plt.xlabel("Input Current")
    plt.ylabel("Eigenvalues")
    plt.axvline(x=iAtBifurcation, color="grey")
    plt.axhline(y=0, color="grey")
    plt.legend()
    plt.grid()
    plt.show()

    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

