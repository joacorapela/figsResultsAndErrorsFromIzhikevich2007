
import sys
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
    xsn = .5
    asn = .25
    xlim = (-5, 5)
    ylim = (-5, 5)
    deltaY = .5
    xs = np.arange(-10, 10, .1)
    asCol = (-3, -1, 0, 1, 3)
    f = lambda x, a: a-x+x**2
    for a in asCol:
        plt.plot(xs, f(x=xs, a=a), label="a=%.02f"%(a), linestyle="dotted")
    plt.plot(xs, f(x=xs, a=asn), label=r"$a_{SN}=%.02f$"%(asn), 
                 linestyle="solid")
    plt.axvline(x=xsn, color="black", linestyle="dashed")
    plt.text(xsn, min(ylim)-deltaY, r"$x_{SN}$")
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.grid()
    plt.legend()
    plt.xlabel("x")
    plt.ylabel(r"$\dot{x}$")
    plt.show()

if __name__=="__main__":
    main(sys.argv)
