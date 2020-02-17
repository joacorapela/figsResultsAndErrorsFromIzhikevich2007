
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):
    t0 = 2
    tf = 10
    dt = 1e-4
    y0 = 2

    def y(t):
        return(1.0/np.tanh(-t+np.arctanh(1/y0)))
    def dy(t):
        return(-1+y(t)**2)

    t = np.arange(t0, tf, dt)
    plt.plot(t, y(t), color="blue", label="y(t)")
    plt.xlabel("Time (sec)")
    plt.ylabel("y(t)")
    plt.legend(loc="upper left")
    ax1 = plt.twinx()
    ax1.plot(t, dy(t), color="green", label="dy(t)")
    ax1.set_ylabel("dy(t)")
    ax1.legend(loc="upper right")
    plt.show()

if __name__=="__main__":
    main(sys.argv)
