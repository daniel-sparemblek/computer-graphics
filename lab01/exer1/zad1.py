import numpy as np
from pyrr import Matrix33, Vector3, matrix33
import math

v1 = Vector3([2., 3., -4.]) + Vector3([-1., 4., -1.])
s = v1 | Vector3([-1., 4., -1.])
v2 = v1 ^ Vector3([2., 2., 4.])

v3 = 0
for x in v2:
    v3 = v3 + x*x
v3 = math.sqrt(v3)

v4 = -v2

m11 = Matrix33([[1., 2., 3.],[2., 1., 3.],[4., 5., 1.]])
m22 = Matrix33([[-1., 2., -3.],[5., -2., 7.],[-4., -1., 3]])
add = m11 + m22

arr1 = np.array([[-1, 2, -3], [5, -2, 7], [-4, -1, 3]])
arr1Trans = arr1.transpose()

m33 = Matrix33(arr1Trans)
mult = matrix33.multiply(m11, m33)

m44 = matrix33.inverse(m22)
inv = matrix33.multiply(m11, m44)



print(v1)
print(" ")
print(s)
print(" ")
print(v2)
print(" ")
print(v3)
print(" ")
print(v4)
print(add)
print(" ")
print(mult)
print(" ")
print(inv)
