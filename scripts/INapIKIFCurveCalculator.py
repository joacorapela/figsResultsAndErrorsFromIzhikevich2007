

class INapIKIFCurveCalculator:
    def calculateIFCurve(self, currents):
        fs = np.empty(len(currents))
        for i in currents:
        
