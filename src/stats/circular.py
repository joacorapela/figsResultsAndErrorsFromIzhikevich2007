import math

def circularVariance(angles):
    c = 0.0
    s = 0.0
    for angle in angles:
        c = c + math.cos(angle)
        s = s + math.sin(angle)
    r = math.sqrt(c**2+s**2)
    v = 1-r/len(angles)
    return(v)
