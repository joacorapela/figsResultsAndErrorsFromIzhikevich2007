#!/bin/csh

if ($#argv == 0) then
    echo "Usage: $0 selfCouplingStrength"
    goto done
endif

set selfCouplingStrength=$1

python doSaveMalkinsWiConstantINapIKLowThresholdWithSelfCoupling.py 0 $selfCouplingStrength
python doSaveMalkinsWiConstantINapIKLowThresholdWithSelfCoupling.py 1 $selfCouplingStrength
python doSaveMalkinsGFuncINapIKLowThresholdWithSelfCoupling.py $selfCouplingStrength
python doSaveMalkinsWConstantINapIKLowThresholdWithSelfCoupling.py $selfCouplingStrength
python doFig10_30INapIKLowThresholdWithSelfCoupling.py $selfCouplingStrength

done:

