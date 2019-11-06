import sympy as sy

x = sy.Symbol('x') 
y = sy.Symbol('y')

3 + sy.sqrt(x) + y ** 2
#>sqrt(x) + y**2 + 3

#       化简; 也可用sympy.simplify()
f = x ** 2 + x **3 - 0.5 * x ** 2 + 7
#>x**3 + 0.5*x**2 + 7



#       解方程; sympy.solve()
##      需要化简为 f(x, y, z) = 0的形式
sy.solve(x ** 3 + 0.5 * x ** 2 - 1)
#>[0.858094329496553, -0.679047164748276 - 0.839206763026694*I, -0.679047164748276 + 0.839206763026694*I]

sy.solve(x ** 3 + 0.5 * x ** 2 - 1 + 2 * x ** 5 - x ** 4)
''' 
[0.783147865018410,
 -0.570005868354481 - 0.486368874890707*I,
 -0.570005868354481 + 0.486368874890707*I,
 0.428431935845276 - 0.976507153271122*I,
 0.428431935845276 + 0.976507153271122*I]
'''

sy.solve(x**2 + y**2)
#>[{x: -I*y}, {x: I*y}]



#       求积分
a = sy.symbols('a'); b = sy.symbols('b')
##      定积分
I = sy.Integral(sy.sin(x) + 0.5 * x, (x, a, b))
print(sy.pretty(I))
'''
b                    
⌠                    
⎮ (0.5⋅x + sin(x)) dx
⌡                    
a 
'''

##      不定积分
I2 = sy.integrate(sy.sin(x) + 0.5 * x, x)
print(sy.pretty(I2)) 
'''
      2         
0.25⋅x  - cos(x)
'''
##      莱布尼茨法则
Fa = I2.subs(x, 0.5).evalf()
Fb = I2.subs(x, 9.5).evalf() 
Fb - Fa
#>24.3747547180867



#       求微分
I2.diff()
#>0.5*x + sin(x)
##      偏微分
f = (sy.sin(x) + x ** 2 + sy.sin(y) + y ** 2)
f_x = f.diff(f, x)
#>2*x + cos(x)
f_y = f.diff(f, y)
#>2*y + cos(y)

## sympy.nsolve()可以用于得到猜测值附近微分函数的零点
## 注意:此方法求极值也是位置敏感的
x0 = sy.nsolve(f_x, -1.5) 
#>-0.450183611294874
y0 = sy.nsolve(f_y, -1.5) 
#>-0.450183611294874
f.subs({x:x0, y:y0}).evalf()
#>-0.464931150316431