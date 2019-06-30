# Used to convert between continuous compounding and compounding
# R1 is continuous compounding interest
# R2 is compounding interest, calculated m times a year
cci <- function (R2, m) {
    R1 = m * log(1 + R2 / m)
    return(R1)
}
# used to convert R2 to R1


ncci <- function (R1, m) {
    R2 = m * exp(R1 / m) - m
    return(R2)
}
