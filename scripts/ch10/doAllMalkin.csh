#!/bin/csh

if ($#argv == 0) then
    echo "Usage: $0 selfCouplingStrength"
    goto done
endif

set selfCouplingStrength=$1

python doSaveMalkinsWiConstantINapIKHighThresholdWithSelfCoupling.py 0 $selfCouplingStrength
python doSaveMalkinsWiConstantINapIKHighThresholdWithSelfCoupling.py 1 $selfCouplingStrength
 python doSaveMalkinsGFuncINapIKHighThresholdWithSelfCoupling.py $selfCouplingStrength
 python doSaveMalkinsWConstantINapIKHighThresholdWithSelfCoupling.py $selfCouplingStrength
 python doFig10_30INapIKHighThresholdWithSelfCoupling.py $selfCouplingStrength

done:

