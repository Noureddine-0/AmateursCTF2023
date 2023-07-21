import z3
import sys


solver = z3.Solver()
length = 0x3d
flag = [z3.BitVec(f"flag_{i}", 8) for i in range(length)]
solver.add(flag[0] == b'a'[0])


with open("headache","rb") as f:
	Content = f.read()
addr = 0x1290


while True :
	if Content[addr+2]==0x3f: #This is because we are working with r15 and rdi registers , so if we found a xor r15b,BYTE PTR[rdi] the instruction in little endian is 44 32 3f else if the assembly contains for example xor r15b,BYTE PTR[rdi+0x2] the machine code will be 44 32 7f 02 , so whenever we dont add an offset to the rdi value the last opcode in these conditions will be 0x3f , note that if we work with other registers the value will not be the same,note also that the offset added to rdi is 1 byte because the len of the flag is less than 0xff(unsigned) , if it wasnt the offset added to the addr in the next_byte few lines will change and not remains 4 because the len of the instruction will not be the same .
		a=0 
		addr +=3
	else :
		a = Content[addr+3]
		addr = addr+4

	if Content[addr+2]==0x3f:
		b=0 
		addr +=3
	else :
		b = Content[addr+3]
		addr = addr+4
	
	cmparison = Content[addr+3]
	addr +=4

	solver.add(flag[a]^flag[b]==cmparison)
	if solver.check() == z3.sat:
		m = solver.model()
		if len(m)==0x3d:
			print(flag := "".join([chr(m[f].as_long()) for f in flag]))
			sys.exit(0)
	if Content[addr]==0x74:#Here you should know how the jump works , in disassembler even if we see je <address> , in the instruction we will not see the address , instead we see an offset off the current r(e)ip, the address is calculated as rip + len(instruction) + offset and we got the instruction that you see in the disassembler.the opcode 0x74 is jump short where the offset is just one byte. 
		jump_offset= Content[addr+1]
		addr +=2
	else :
		jump = Content[addr:addr+6]
		jump_offset = int.from_bytes(jump[2:],"little",signed=True)
		addr+=6
	addr += jump_offset


	xor = Content[addr:addr+5]
	xor = int.from_bytes(xor[1:], "little")
	addr +=5
	lea = Content[addr: addr + 8]
	lea = int.from_bytes(lea[4:], "little", signed=True)

	addr  = int(hex(lea)[4:],16)

	i=addr
	decoded= b""
	while True:
		next_byte = int.from_bytes(Content[i: i + 4], "little")
		if next_byte == 0:
			break
		next_byte ^= xor
		decoded += next_byte.to_bytes(4, "little")
		i += 4
	Content = Content[:addr] + decoded + Content[addr + len(decoded):]

