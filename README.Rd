Reproduction of figures, results and errors from Izhikevich 2007
================================================================

python code on dynamical systems reproducing many figures, results and errors
from Izhikevich 2007. This code is still unorganized.

Izhikevich, E. M. (2007). Dynamical systems in neuroscience. MIT press.

This code was written with python 2.7.

For example, to reproduce Figure 4.4, from the "test/" directory, run:

python2.7 doFig4-4.py 

To generate some figures you might have to run an integration before. For
example, to reproduce Figure 10.10b "test/ch10/" directory, run:

python2.7 doIntegrateINapIKFig10_1_INapIKHighThreshold.py

and then:

python2.7 doFig10_1b.py

The figures will be saved under the directory figures.

The "reports" directory contains reports on:

1. the saddle-node bifurcation (anBifNormalForm.ps),

2. Andronov-Hopf bifurcation (andronovHopfBifurcation.ps),

3. a typo on "Section 6.1.3 Supercritical Andronov-Hopf" of Izhikevich 2007
(typoSec6.1.3.pdf),

4. verification of Malkins theorem and problems I found on Figures 20-26 and
10-30a of Izhikevich 2007 (malkinTheorem.pdf).

Code for generating the figures in these reports appears under the "test/" or
"test/ch10" directories.

