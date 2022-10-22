//openssl ec -in ecprivkey.pem -pubout -out ecpubkey.pem
module point_mult_testbench();

timeunit 10ns;	// Half clock cycle at 50 MHz
			// This is the amount of time represented by #1
timeprecision 1ns;

logic Clk, Reset;
logic [255:0] Py, Px, Rx, Ry, k;
logic Done;

point_mul p(.P({Px, Py}), .R({Rx, Ry}), .clk(Clk), .*);

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
Px = 4'd6;
Py = 4'd1;
k = 4'd5;
Reset = 1'b1;
#2 Reset = 1'b0;
end

endmodule
