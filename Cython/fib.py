#   Input in Linux Shell below:
#   python setup.py build_ext --inplace
##      a file called 'fib.cpython-37m-x86_64-linux-gnu.so' should be generated in the path with fib.pyx file

#   With pyx name 'fib', now we could directly import it in python environment
import fib
fib?
'''
Type:        module
String form: <module 'fib' from '/home/sariel/Quant/Cython/fib.cpython-37m-x86_64-linux-gnu.so'>
File:        ~/Quant/Cython/fib.cpython-37m-x86_64-linux-gnu.so
Docstring:   <no docstring>
'''

fib.fib?
'''
Docstring: <no docstring>
Type:      builtin_function_or_method
'''

%%time 
fib.fib(1000)
'''
CPU times: user 7 µs, sys: 1e+03 ns, total: 8 µs
Wall time: 11.4 µs
Out[12]: 4.346655768693743e+208
'''

#   Set a raw python version to compare the speed
def fib_py(n):
    a=0; b=1
    for i in range(n):
        a, b = a+b, a
    return a

%%time
fib_py(1000)
'''
CPU times: user 53 µs, sys: 10 µs, total: 63 µs
Wall time: 63.9 µs
Out[15]: 43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875
'''
#       So we see a 6 time boost from Cython version


#   Module 'pyximport' could also be used for the same puropse
## 'fib.pyx' should be in the same path with ipython environment
import pyximport
pyximport.install()
'''
(None, <pyximport.pyximport.PyxImporter at 0x123454a80>)
'''
import fib
#   Now fib.fib could be used as above example






