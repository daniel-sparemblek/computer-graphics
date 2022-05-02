import numpy as np
txt = input("Upišite jednadžbe sa zarezom između: ")

splitText = txt.split(",")
vector1 = [None]*3
vector2 = [None]*3
vector3 = [None]*3
b = [None]*3
vector1[0] = int(splitText[0])
vector1[1] = int(splitText[1])
vector1[2] = int(splitText[2])
vector2[0] = int(splitText[4])
vector2[1] = int(splitText[5])
vector2[2] = int(splitText[6])
vector3[0] = int(splitText[8])
vector3[1] = int(splitText[9])
vector3[2] = int(splitText[10])
b[0] = int(splitText[3])
b[1] = int(splitText[7])
b[2] = int(splitText[11])

a = np.array([vector1, vector2, vector3])
x = np.linalg.solve(a, b)

print(x)
