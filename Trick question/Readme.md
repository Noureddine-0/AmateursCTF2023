# AmateursCTF 2023

## Trick question

>Which one do you hate more: decompiling pycs or reading Python bytecode disassembly? Just kidding that's a trick question.
>
>Run with Python version 3.10.
>
>Flag is amateursCTF{[a-zA-Z0-9_]+}
>
>Author:flocto


The challenge is given a pyc program compiled with Python version3.10 , since this is the first time i encounter a pyc program i found some problems solving the challenge.I started by learning some bytecode instructions using the dis module in python , after this i found a great tool named pydisasm that was the first push in this challenge , i'll try to make the solution simple so let's start by opening a terminal and typing ```pydisasm <the_pyc_program>```
We found two tuple where the first contains zeroes and ones and the second holds some base64 encoded strings , lookin at the disassembly we saw that the program creates two lists where each contains the content of a tuple :
```

   1:         8 BUILD_LIST           0
              10 LOAD_CONST         (zeroes and ones)  
              12 LIST_EXTEND          1
              14 STORE_NAME           (r)
   2:         16 BUILD_LIST           0
              18 LOAD_CONST          (base64 encoded data)
              20 LIST_EXTEND          1
              22 STORE_NAME           (x)
```
After that we saw a for loop that iterates on the r list which contains the zeroes and ones , if the element popped from the evaluation stack is 0 it continues , otherwise it reverses the string x[i], after iterating over all the elements of r it reverse x , join its elements with 'A' , decode the content with the b64decode (Note that it uses a function named b64decode which make use of b64decode method of the base64 module) function .
```
3:          24 LOAD_NAME            (range)
              26 LOAD_NAME            (len)
              28 LOAD_NAME            (r)
              30 CALL_FUNCTION        (1 positional argument)
              32 CALL_FUNCTION        (1 positional argument)
              34 GET_ITER
         >>   36 FOR_ITER             (to 72)
              38 STORE_NAME           (i)

  7:          40 LOAD_NAME            (r)
              42 LOAD_NAME            (i)
              44 BINARY_SUBSCR
              46 POP_JUMP_IF_FALSE    (to 70)

  8:          48 LOAD_NAME            (x)
              50 LOAD_NAME            (i)
              52 BINARY_SUBSCR
              54 LOAD_CONST           (None)
              56 LOAD_CONST           (None)
              58 LOAD_CONST           (-1)
              60 BUILD_SLICE          3
              62 BINARY_SUBSCR
              64 LOAD_NAME            (x)
              66 LOAD_NAME            (i)
              68 STORE_SUBSCR

  9:     >>   70 JUMP_ABSOLUTE        (to 36)

-119:     >>   72 LOAD_NAME            (b64decode)
              74 LOAD_CONST           ('A')
              76 LOAD_METHOD          (join)
              78 LOAD_NAME            (x)
              80 LOAD_CONST           (None)
              82 LOAD_CONST           (None)
              84 LOAD_CONST           (-1)
              86 BUILD_SLICE          3
              88 BINARY_SUBSCR
              90 CALL_METHOD          1
              92 CALL_FUNCTION        (1 positional argument)
              94 POP_TOP
              96 LOAD_CONST           (None)
              98 RETURN_VALUE
```
because we are reversing the program we only need the output so we catch it and its there where the author gives a hint to continue and its the use of pycdc decompiler to decompile Code objects (Note that at first time i had no idea about pycdc or i could simply use it to decompile the pyc challenge), the output contains a Code object that we need to decompile but i wasnt able to decompile it that's why i got the idea of using it to creat a pyc file then use pycdc,i'll put the script to create the pyc file <a href="https://github.com/Noureddine-0/AmateursCTF2023/blob/main/Trick%20question/script.py">here</a> , just after decompiling we got a python code that we could simply <a href="https://github.com/Noureddine-0/AmateursCTF2023/blob/main/Trick%20question/solve.py">reverse</a>.

## Solution
```amateursCTF{PY7h0ns_ar3_4_f4m1lY_0f_N0Nv3nom0us_Sn4kes}```
