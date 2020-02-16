
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel
from utils import buildMatrixFromArraysList

def main(argv):
    i0 = 10.0

    v0 = -60.00
    n0 = 0.0008
    t0 = 0.0
    tf = 140.0
    dt = 1e-4
    current0 = 0.0
    timeWinToSearchForUnstableFocus = (10, 80)

    iSlope = 30.0/100.0
    def i(t, iSlope=iSlope):
        return(current0+iSlope*t)
    iNapIKModel = INapIKModel.getLowThresholdInstance(i=i)
    integrator = ode(iNapIKModel.deriv).set_integrator('vode', max_step=dt)

    y0 = [v0, n0]
    integrator.set_initial_value(y0, t0)
    ys = [y0]
    times = [t0]
    stabilityType, eigenValues, jacobian = \
     iNapIKModel.checkStability(v0=v0, n0=n0)
    stabilityTypes = [stabilityType]
    eigenValuesList = [eigenValues.tolist()]
    jacobiansList = [jacobian.flatten().tolist()]
    step = 0
    t = t0
    y = y0
    successfulIntegration = True
    while successfulIntegration and t<tf:
        step = step + 1
        if step%10==0:
            print('Processing time %.05f out of %.02f (i=%.02f)' % (t, tf, i(t=t)))
            sys.stdout.flush()
        integrator.integrate(t+dt)
        t = integrator.t
        y = integrator.y
        times.append(t)
        ys.append(y.tolist())
        v = y[0]
        n = y[1]
        stabilityType, eigenValues, jacobian = \
         iNapIKModel.checkStability(v0=v, n0=n)
        stabilityTypes.append(stabilityType)
        eigenValuesList.append(eigenValues.tolist())
        jacobiansList.append(jacobian.flatten().tolist())
    timesArray = np.array(times)
    ysArray = buildMatrixFromArraysList(arraysList=ys)
    eigenValuesArray = buildMatrixFromArraysList(arraysList=eigenValuesList)
    stabilityTypesArray = np.array(stabilityTypes)
    unstableFocusIndices = np.where(stabilityTypesArray==
                                     iNapIKModel.UNSTABLE_FOCUS)[0]
    timeWinIndices = np.where(np.logical_and(timeWinToSearchForUnstableFocus[0]<=timesArray, timesArray<=timeWinToSearchForUnstableFocus[1]))[0]
    validUnstableFocusIndices = np.intersect1d(ar1=unstableFocusIndices, ar2=timeWinIndices)
    bifurcationIndex = validUnstableFocusIndices[0]
    iAtBifurcation = i(t=timesArray[bifurcationIndex])
    jacobianAtBifurcation = np.reshape(a=jacobiansList[bifurcationIndex],
                                        newshape=(2,2))
    print("Input current at bifurcation: %.08f"%iAtBifurcation)
    print("V at bifurcation: %.08f"%(ysArray[0,bifurcationIndex]))
    print("n at bifurcation: %.08f"%ysArray[1,bifurcationIndex])
    print("Jacobian at bifurcation: [[%.08f,%.08f],[%.08f,%.08f]]"%
           (jacobianAtBifurcation[0,0], jacobianAtBifurcation[0,1],
            jacobianAtBifurcation[1,0], jacobianAtBifurcation[1,1]))
    print("Eigenvalues at bifurcation: %.08f+j%.08f, %.08f+j%.08f"%
          (eigenValuesArray[0,bifurcationIndex].real,
            eigenValuesArray[0,bifurcationIndex].imag,
            eigenValuesArray[1,bifurcationIndex].real,
            eigenValuesArray[1,bifurcationIndex].imag))

    plt.plot(i(timesArray), eigenValuesArray[0,:].real)
    plt.xlabel("Input Current")
    plt.ylabel("Real Part of Eigenvalues")
    plt.axhline(y=0, color="grey")
    plt.axvline(x=iAtBifurcation, color="grey")
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

