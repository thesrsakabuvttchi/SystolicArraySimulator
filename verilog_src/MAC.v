`include "FPM.v"

module MAC(input [31:0] a,b,c,
        input clk,
        output [31:0]out);
    wire [31:0] buffer;
    FPMul multiplier(clk,a,b,buffer);
    FPAdder adder(clk,buffer,c,out);
endmodule

