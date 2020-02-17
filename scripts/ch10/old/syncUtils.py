
import pdb
import numpy as np
from signalProcessingUtils import lowpassKaiser
from utils import getPeakIndices

def getPhasesFromVoltages(voltages, sampleRate, 
                                    cutoffHz=4, transitionWidthHz=1.0, 
                                    rippleDB=60, doPlots=False):
    lpVoltages = lowpassKaiser(x=voltages, cutoffHz=cutoffHz, 
                                           transitionWidthHz=transitionWidthHz,
                                           rippleDB=rippleDB,
                                           sampleRate=sampleRate,
                                           doPlots=doPlots)
    spikeIndices = getPeakIndices(v=lpVoltages)
    voltageIndices = range(len(voltages))
    numberOfSamplesSincePreviousSpike = np.empty(len(voltages))
    lastSpikeIndex = 0
    for nextSpikeIndex in spikeIndices:
        voltageIndicesBtwLastAndNextSpikeIndex = np.nonzero(np.logical_and(lastSpikeIndex<=voltageIndices, voltageIndices<nextSpikeIndex))[0]
        numberOfSamplesSincePreviousSpike[voltageIndicesBtwLastAndNextSpikeIndex] = voltageIndicesBtwLastAndNextSpikeIndex-lastSpikeIndex
        lastSpikeIndex = nextSpikeIndex
    phases = numberOfSamplesSincePreviousSpike/sampleRate
    return(phases)
