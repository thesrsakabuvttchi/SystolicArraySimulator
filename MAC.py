import os
import struct
from typing import List

def to_int(x : float):
    return struct.unpack('I', struct.pack('f', float(x)))[0]  

def to_float(x : float):
    return struct.unpack('f', struct.pack('I', x))[0]   

class MAC:
    def __init__(self) -> None:
        self.reg_a = 0
        self.reg_result = 0
    # Input, W, C-res from prev
    def MAC(self,x : float, y : float, z : float):
        f_out = open('input.txt','w')
        integers = [to_int(x),to_int(y),to_int(z)]
        f_out.write(','.join([str(i) for i in integers]))
        f_out.close()
        
        os.system('./verilog_src/a.out')
        f_in = open('output.txt','r')
        result = to_float(int(f_in.read()))

        self.reg_a = x
        self.reg_result = result
        return(result)
    def MAC_list(self,x_list : List[float], y_list : List[float], z_list : List[float]):
        f_out = open('input.txt','w')
        for i in range(len(x_list)):
            x = x_list[i]
            y = y_list[i]
            z = z_list[i]
            integers = [to_int(x),to_int(y),to_int(z)]
            f_out.write(','.join([str(i) for i in integers])+'\n')

        
        f_out.close()
        os.system('./verilog_src/a.out')
        f_in = open('output.txt','r')
        result = [to_float(int(i)) for i in f_in.read().strip('\n').split('\n')]

        return(result)
