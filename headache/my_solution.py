import r2pipe
import z3
import sys
solver = z3.Solver()
length  = 0x3d
flag = [z3.BitVec(f"flag_{i}",8) for i in range(length)]
solver.add(flag[0] ==b'a'[0])
r2 = r2pipe.open("./headache")
r2.cmd(" e dbg.profile=headache.rr2")
r2.cmd("doo")
r2.cmd("db 0x401290")
r2.cmd("dc")

def step():
	r2.cmd("ds")
	r2.cmd("sr rip")

offsets = [0]*2
while True:
	for i in range(2):
		current_instruction = r2.cmdj("pdj 1")[0]
		offset = current_instruction["opcode"].split("rdi")[1].split(" +")[-1].split("]")[0]
		if not offset:
			offsets[i] = 0
		else:
			offsets[i] = int(offset,16)

		step()

	print(offsets[0] , offsets[1])
	comparison = r2.cmdj("pdj1")[0]["opcode"].split(', ')[-1]
	if not comparison:
		comparison = 0
	else:
		comparison = int(comparison ,16)

	solver.add(flag[offsets[0]] ^ flag[offsets[1]] ==comparison)
	if solver.check() == z3.sat:
		m = solver.model()
		if len(m)==0x3d:
			print(flag := "".join([chr(m[f].as_long()) for f in flag]))
			sys.exit(0)

	step()
	r2.cmd("dr zf=1")#To pass the check in the cmp instruction 
	step()

	while True:
		current_instruction = r2.cmdj("pdj 1")
		if current_instruction[0]['type'] =='call':
			step()
			break

		step()
