#requires ipython and cython
%load_ext Cython
# Caution: cythonmagic has been moved to cython package, not in ipython anymore, so %load_ext cythonmagic will not work
%%cython
def fib(int n):
    cdef int n
    cdef double a=0.0, b= 1.0
    for i in range(n):
        a, b = a+b, a
    return a
