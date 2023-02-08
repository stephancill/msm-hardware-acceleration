import elliptic_curve_structs::*;

module multiplier_testbench();

timeunit 10ns;	// Half clock cycle at 50 MHz
			// This is the amount of time represented by #1 
timeprecision 1ns;

logic Clk, Reset, Done;
logic [P_WIDTH-1:0] a, b, product;

MultiplierAdapter mult0(.clk(Clk), .*);

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
Reset = 1'b1;
#2 Reset = 1'b0;
//EXPECTED: 33
end

endmodule
