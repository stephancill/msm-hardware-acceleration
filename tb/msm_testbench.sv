import elliptic_curve_structs::*;

module msm_testbench();

timeunit 10ns;	// Half clock cycle at 50 MHz
			// This is the amount of time represented by #1
timeprecision 1ns;

localparam MSM_LENGTH = 100;

logic clk, Reset;
logic [P_WIDTH-1:0] Rx, Ry;
logic [P_WIDTH-1:0] test_Rx [0:0];
logic [P_WIDTH-1:0] test_Ry [0:0];
logic [P_WIDTH-1:0] Gx [MSM_LENGTH-1:0];
logic [P_WIDTH-1:0] Gy [MSM_LENGTH-1:0];
curve_point_t G [MSM_LENGTH-1:0];
logic [SCALAR_WIDTH-1:0] x [MSM_LENGTH-1:0];
logic Done;

msm_naive #(.length(MSM_LENGTH)) msm (.G(G), .x(x), .R({Rx, Ry}), .*);
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
// 'test_Gx.txt' G.x
// 'test_Gy.txt' G.y
// 'text_x.txt' x
// Each file has 100 lines, loop over them and use $readmemh to read them in
$readmemh("test_Gx.txt", Gx);
$readmemh("test_Gy.txt", Gy);
$readmemh("test_x.txt", x);
$readmemh("test_Rx.txt", test_Rx);
$readmemh("test_Ry.txt", test_Ry);

// Populate G
for (int i = 0; i < MSM_LENGTH; i++) begin
    G[i].x = Gx[i];
    G[i].y = Gy[i];
end

Reset = 1'b1;
#2 Reset = 1'b0;

forever begin
    if (Done) begin
        assert (Rx == test_Rx[0]);
        assert (Ry == test_Ry[0]);
        $finish;
    end else
        #1;
end
end

endmodule
