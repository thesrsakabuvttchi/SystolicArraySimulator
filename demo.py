import randgen
import tiling
import conv
import numpy as np
import os
f = open('instructions.ss','w')
f.close()
print("Demo for Systolic Array Simulator V1.0 By Srinivasan and Shanjeev!\n")
print("Test (1/3) Martxix Multiply..........................................................")
randgen.init_matrices()
host = tiling.hostcaller(4)
host.tiler()

print('press any key to continue......')
input()
try:
    host.sysobj.root.destroy()
except:
    pass

os.system('clear')
print("\nTest (2/3) Print Generated assembley..........................................................")
f = open('instructions.ss')
print(f.read())
print('press any key to continue......')
input()

os.system('clear')
print("\nTest (3/3) Convolution..........................................................")
I = np.array([[1, 2, 3], [4, 5, 6]])
F = np.array([[10, 20], [30, 40]])
print(conv.convolution_as_maultiplication(I,F))