`include "MAC.v"

module top;
reg [31:0]a, b, c;
wire [31:0]ans;
reg clk;
integer ip_file,out_file,r;
MAC testmult(a,b,c,clk,ans);

initial
begin
    ip_file = $fopen("input.txt","r");
    out_file = $fopen("output.txt","w");
    while (! $feof(ip_file)) begin
        r = $fscanf(ip_file,"%d,%d,%d\n",a,b,c);
        #1 $fwrite(out_file,"%d\n",ans);
    end 
    $fclose(out_file);
end
endmodule
