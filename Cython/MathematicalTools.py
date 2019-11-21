%%cython 
cdef class Particle: 
        cdef public double mass 
        cdef readonly double position 
        cdef double velocity 
        def __init__(self, m, p, v): 
                self.mass = m 
                self.position = p 
                self.velocity = v 
        def get_momentum(self): 
                 return self.mass * self.velocity 


%%cythhon 
cdef class Matrix: 
        cdef: 
                unsigned int nrows, ncols 
                double *_matrix 
        def __cinit__(self, nr, nc): 
                self.nrows = nr 
                self.ncols = nc 
                self._matrix = <double*>mallo(nr * nc * sizeof(double))
                if self._matrix == NULL:
                        raise MemoryError()
        def __dealloc__(self):
                if self._matrix != NULL:
                        free(self._matrix) 