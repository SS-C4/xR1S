import math
import sys

if len(sys.argv) > 1:
	m = int(sys.argv[1])
else:
	m = 4

#No degree support yet
#2^m - 1 on each branch (m -> height)
n = 3*(2**m - 1) + 1

g1 = [[] for i in range(n)]

#center
g1[0] = [1, 1 + (2**m - 1), 1 + 2*(2**m -1)]

#branch 1
for i in range(1, 2**(m-1)):
	g1[i] = [int(i/2), i*2, i*2+1]
#leaves
for i in range(2**(m-1), 2**m):
	g1[i] = [int(i/2)]

#branch 2
for i in range(1, 2**(m-1)):
	g1[(2**m - 1) + i] = [(2**m - 1) + int(i/2), (2**m - 1) + i*2, (2**m - 1) + i*2+1]
#leaves
for i in range(2**(m-1), 2**m):
	g1[(2**m - 1) + i] = [(2**m - 1) + int(i/2)]

#branch 3
for i in range(1, 2**(m-1)):
	g1[2*(2**m - 1) + i] = [2*(2**m - 1) + int(i/2), 2*(2**m - 1) + i*2, 2*(2**m - 1) + i*2+1]
#leaves
for i in range(2**(m-1), 2**m):
	g1[2*(2**m - 1) + i] = [2*(2**m - 1) + int(i/2)]

#correction for first attachment
g1[1 + (2**m -1)][0] = 0
g1[1 + 2*(2**m - 1)][0] = 0

f = open("large", "w")
for num, i in enumerate(g1):
	f.write (str(num) + " " + " ".join(str(j) for j in g1[num]) + '\n')

f.close()