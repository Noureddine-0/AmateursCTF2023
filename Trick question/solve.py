from z3 import *
import random
import hashlib
import string

printable  =string.printable
Listed_flag = []
Listed_flag.append("sn0h7YP"[::-1])
#Solve system
x,y,z = Ints('x y z')
solver = Solver()
solver.add(x+y-z==160)
solver.add(y+z-x==68)
solver.add(z+x-y==34)
if solver.check()==sat:
	model=solver.model()
	Listed_flag.append("".join(chr(model[i].as_long()) for i in model)[::-1])
for i in printable:
	if hashlib.sha256(i.encode()).hexdigest()=='4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a':
		Listed_flag.append(i)
		random.seed(i.encode())
		break
random.shuffle(L:=[i for i in range(6)])
list1=[49, 89, 102, 109, 108, 52]
list2=[]
for i in range(6):
	index = L.index(i)
	list2.append(chr(list1[index]))
Listed_flag.append("".join(list2))
Listed_flag.append('0f')
list3 = [random.randint(0,0xFFFFFFFF) for i in range(3)]
list4 = [0xFBFF4501, 825199122, 0xFEEF2AA6]
Listed_flag.append("".join([int.to_bytes(i^j,4,'little').decode() for i,j in zip(list3,list4)])[:-1])
c = 0x29ee69af2f3
byte_string = b""
while c:
    byte_string += bytes([c % 128])
    c //= 128
Listed_flag.append(byte_string.decode()[::-1])

print("amateursCTF{"+ "_".join(Listed_flag) + "}")

