import numpy as np
vector1 = [None]*3
vector2 = [None]*3
vector3 = [None]*3
vector4 = [None]*3
txt = input("Upišite koordinate točke A: ")
splitText = txt.split(",")
vector1[0] = int(splitText[0])
vector2[0] = int(splitText[1])
vector3[0] = int(splitText[2])

txt = input("Upišite koordinate točke B: ")
splitText = txt.split(",")
vector1[1] = int(splitText[0])
vector2[1] = int(splitText[1])
vector3[1] = int(splitText[2])

txt = input("Upišite koordinate točke C: ")
splitText = txt.split(",")
vector1[2] = int(splitText[0])
vector2[2] = int(splitText[1])
vector3[2] = int(splitText[2])

txt = input("Upišite koordinate točke T: ")
splitText = txt.split(",")
vector4[0] = int(splitText[0])
vector4[1] = int(splitText[1])
vector4[2] = int(splitText[2])

a = np.array([vector1, vector2, vector3])
x = np.linalg.solve(a, vector4)

print(x)
