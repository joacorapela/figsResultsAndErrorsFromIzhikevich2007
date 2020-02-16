#!/bin/csh

set phaseIndices=(7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37)
set nPhases=40

foreach phaseIndex ($phaseIndices)
    echo "Processing phase $phaseIndex ($nPhases)"
    python doSaveIsochron.py $phaseIndex $nPhases
end
