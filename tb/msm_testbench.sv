import elliptic_curve_structs::*;

module msm_testbench();

timeunit 10ns;	// Half clock cycle at 50 MHz
			// This is the amount of time represented by #1
timeprecision 1ns;

localparam length = 3;

logic clk, Reset;
logic [255:0] Rx, Ry;
curve_point_t G [length-1:0];
logic [255:0]	x [length-1:0];
logic Done;

msm_naive #(.length(length)) msm (.G(G), .x(x), .R({Rx, Ry}), .*);
// Toggle the clock
// #1 means wait for a delay of 1 timeunit
always begin : CLOCK_GENERATION
#1 clk = ~clk;
end

initial begin: CLOCK_INITIALIZATION
    clk = 0;
end

//Testing
initial begin: TEST_VECTORS
//Initialize signals
// points = [(6, 1), (17, 6), (5, 13)]
// scalars = [18, 80, 17] # (24, 17), (13, 24), (19, 24)
G[0].x = 6;
G[0].y = 1;
G[1].x = 17;
G[1].y = 6;
G[2].x = 5;
G[2].y = 13;

x[0] = 18;
x[1] = 80;
x[2] = 17;

Reset = 1'b1;
#2 Reset = 1'b0;

forever begin
    if (Done) begin
        assert (Rx == 35);
        assert (Ry == 6);
        $finish;
    end else
        #1;
end
end

endmodule
