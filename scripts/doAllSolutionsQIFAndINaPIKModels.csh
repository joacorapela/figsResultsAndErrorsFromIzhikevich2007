#!/bin/csh

if ($#argv != 2) then
    echo "Usage: $0 tauV i0"
    goto done
endif

set tauV = $1
set i0 = $2
python doSaveSolutionQuadraticIFModel.py {$i0}
python doIntegrateINapIKFig6-07.py {$tauV} {$i0}
python doPlotSolutionsQIFAndINaPIKModels.py {$tauV} {$i0}

done:
 exit 0

