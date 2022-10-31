import elliptic_curve_structs::*;

module add_testbench();

timeunit 10ns;	// Half clock cycle at 50 MHz
			// This is the amount of time represented by #1 
timeprecision 1ns;

logic Clk, Reset, Done, op;
logic [P_WIDTH-1:0] a, b, sum;

add add(.*);

// Toggle the clock
// #1 means wait for a delay of 1 timeunit
always begin : CLOCK_GENERATION
#1 Clk = ~Clk;
end

initial begin: CLOCK_INITIALIZATION
    Clk = 0;
end 

//Testing
initial begin: TEST_VECTORS
//Initialize signals
a = 123;
b = 456;
op = 1'b0;

assert (sum == 579);

a = 456;
b = 123;
op = 1'b1;

assert (sum == 333);
//EXPECTED: 0x1200
//#200000 Reset = 1'b1;
//#2 Reset = 1'b0;
//a = 256'h09;
//b = 256'hFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFE2F;
end

endmodule
