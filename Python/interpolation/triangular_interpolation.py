import numpy as np
import sys

if len(sys.argv) != 6:
    print("Usage: python triangular_interpolation.py [x1,y1] [x2,y2] [x3,y3] [xA,yA] [z1, z2, z3]")
    sys.exit(1)

nodes = sys.argv
nodes = np.array([list(map(int, node[1:-1].split(','))) for node in sys.argv[1:-1]], dtype=int)

# Calculate the area
n = nodes[0:3]
n1 = n[0]
n2 = n[1]
n3 = n[2]
area = 0.5 * np.abs(n1[0]*(n2[1]-n3[1]) + n2[0]*(n3[1]-n1[1]) + n3[0]*(n1[1]-n2[1]))

print("Area =", area)

xA, yA = nodes[3]
z = list(map(int, sys.argv[5][1:-1].split(',')))
interpolationFunc = [None] * 3

result = 0
for i in range(3):
    result += z[i]*((1/(2*area))*((n[(i+1)%3][0]*n[(i+2)%3][1]-n[(i+2)%3][0]*n[(i+1)%3][1])+xA*(n[(i+1)%3][1]-n[(i+2)%3][1])+yA*(n[(i+2)%3][0]-n[(i+1)%3][0])))

print("Result =", np.abs(result))