
import sys
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
    xsn1 = -1.0
    asn1 = 2.0
    xsn2 = 1.0
    asn2 = -2.0
    xlim = (-5, 5)
    ylim = (-5, 5)
    deltaY = .5
    xs = np.arange(-10, 10, .1)
    asCol = (-3, -1, 0, 1, 3)
    f = lambda x, a: 1+a*x+x**2
    for a in asCol:
        plt.plot(xs, f(x=xs, a=a), label="a=%.02f"%(a), linestyle="dotted")
    plt.plot(xs, f(x=xs, a=asn1), label=r"$a_{SN1}=%.02f$"%(asn1), 
                 linestyle="solid")
    plt.plot(xs, f(x=xs, a=asn2), label=r"$a_{SN2}=%.02f$"%(asn2), 
                 linestyle="solid")
    plt.axvline(x=xsn1, color="black", linestyle="dashed")
    plt.text(xsn1, min(ylim)-deltaY, r"$x_{SN1}$")
    plt.axvline(x=xsn2, color="black", linestyle="dashed")
    plt.text(xsn2, min(ylim)-deltaY, r"$x_{SN2}$")
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.grid()
    plt.legend()
    plt.xlabel("x")
    plt.ylabel(r"$\dot{x}$")
    plt.show()

if __name__=="__main__":
    main(sys.argv)
