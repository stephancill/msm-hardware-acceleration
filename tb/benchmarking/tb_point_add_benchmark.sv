import elliptic_curve_structs::*;

module tb_point_add_benchmark();

timeunit 10ns;	// Half clock cycle at 50 MHz
			// This is the amount of time represented by #1
timeprecision 1ns;

localparam LENGTH = 100;

logic clk, Reset, Done;
logic [P_WIDTH-1:0] test_Rx [LENGTH-1:0];
logic [P_WIDTH-1:0] test_Ry [LENGTH-1:0];
logic [P_WIDTH-1:0] test_Px [LENGTH-1:0];
logic [P_WIDTH-1:0] test_Py [LENGTH-1:0];
logic [P_WIDTH-1:0] test_Qx [LENGTH-1:0];
logic [P_WIDTH-1:0] test_Qy [LENGTH-1:0];
curve_point_t Ps [LENGTH-1:0];
curve_point_t Qs [LENGTH-1:0];
curve_point_t Rs [LENGTH-1:0];

curve_point_t P, Q, R;

logic [$clog2(LENGTH)-1:0] counter;


point_add point_add (.P(P), .Q(Q), .R(R), .*);
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
$readmemh("test_Px.txt", test_Px);
$readmemh("test_Py.txt", test_Py);
$readmemh("test_Qx.txt", test_Qx);
$readmemh("test_Qy.txt", test_Qy);
$readmemh("test_Rx.txt", test_Rx);
$readmemh("test_Ry.txt", test_Ry);

// Populate points
for (int i = 0; i < LENGTH; i++) begin
    Ps[i].x = test_Px[i];
    Ps[i].y = test_Py[i];
    Qs[i].x = test_Qx[i];
    Qs[i].y = test_Qy[i];
    Rs[i].x = test_Rx[i];
    Rs[i].y = test_Ry[i];
end

counter = 0;

P = Ps[counter];
Q = Qs[counter];
Reset = 1'b1;
#2 Reset = 1'b0;

forever begin
  // Wait for done to go high, test the result, and then reset
  if (Done) begin
    if (R.x != Rs[counter].x || R.y != Rs[counter].y) begin
      $display("Test failed at counter = %0d", counter);
      $display("R.x = %0h, Rs.x = %0h", R.x, Rs[counter].x);
      $display("R.y = %0h, Rs.y = %0h", R.y, Rs[counter].y);
      $finish;
    end
    counter = counter + 1;
    $display("Test %d passed", counter);
    if (counter == LENGTH) begin
      $display("All tests passed");
      $finish;
    end
    P = Ps[counter];
    Q = Qs[counter];
    Reset = 1'b1;
    #2 Reset = 1'b0;
  end else begin 
    #1;
  end
end
end

endmodule
