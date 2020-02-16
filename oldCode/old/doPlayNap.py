
processAll <- function() {
    v <- seq(from=-100, to=40, by=1)
    i <- -100

    f <- f_Nap(v, i)

    plot(v, f, xlab="V (mV)", ylab=sprintf("F(V, I=%.1f)", i), type="l")
    abline(h=0)
}

f_Nap <- function(v, i, gL=19, eL=-67, gNa=74, eNa=60, v0.5=1.5, k=16, c=10) {
    f = (i - gL*(v-eL)-gNa*mInf(v, v0.5=v0.5, k=k)*(v-eNa))/c
    return(f)
}

mInf <- function(v, v0.5=1.5, k=16) {
    return(1/(1+exp((v0.5-v)/k)))
}

processAll()

rm(processAll, f_Nap, mInf)
