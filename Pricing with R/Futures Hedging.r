# For long side: $ return = (S_0 - S_t) + h(F_{t,T} - F_{0,T}) $
dtttb = function(svar, fvar, cov, s0, st, f0, ft) {
        h = cov/fvar
        r = s0 - st + h*(ft - f0)
        var = svar + h^2 * fvar - 2*h*cov
        cat('Optimal long hedge ratio h:', h, '\n')
        cat('Return of hedge:', r, '\n')
        cat('Var of long hedge:', var, '\n')
}

ktttb = function(svar, fvar, cov, s0, st, f0, ft) {
        h = cov/fvar
        r = st - s0 - h*(ft - f0)
        var = svar + h^2 * fvar - 2*h*cov
        cat('Optimal short hedge ratio h:', h, '\n')
        cat('Return of hedge:', r, '\n')
        cat('Var of long hedge:', var, '\n')
}








