
import sys
from myMath import findZeroByBisection

def main(argv):
    f = lambda x: -(x**2-1)
    zero = findZeroByBisection(f=f, xMin=-10.0, xMax=-.1)
    print('zero=%f'%zero)

if __name__ == "__main__":
    main(sys.argv)

