%%timeit
import numpy.random as npr
a = list(npr.random(1000000))
for i in range(1, len(a)-1):
    a[i] = (a[i-1]+a[i]+a[i+1])/3
'''
707 ms ± 16.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
'''

%%timeit
%%cython
import numpy.random as npr
cdef list A = list(npr.random(1000000))
cdef unsigned int i
for i in range(1, len(A)-1):
    A[i] = (A[i-1]+A[i]+A[i+1])/3
'''
517 µs ± 6.28 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
'''