import elliptic_curve_structs::*;
module point_mult_double_add_testbench();

timeunit 10ns;	// Half clock cycle at 50 MHz
			// This is the amount of time represented by #1
timeprecision 1ns;

logic Clk, Reset;
logic [P_WIDTH-1:0] Py, Px, Rx, Ry, k;
logic Done;

logic [7:0] counter;

point_mul_double_and_add p(.P({Px, Py}), .R({Rx, Ry}), .clk(Clk), .*);

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
// Px = params.base_point.x;
// Py = params.base_point.y;
// k = 254'h3b90f1f8dc6b19b59ca39e6aa82bcd0d53376d493c6ac111fe6686d14192f6d6;
counter = 0;
Px = 6;
Py = 36;
k = 38;

Reset = 1'b1;
#2 Reset = 1'b0;

forever begin
  if (Done) begin
    // assert (Rx == 377'he195836abff608bdc9f44529e31c5f0fec56d3ec60898894532bbe31b5626a6c543a901dd64b498674c9b1d413a76e);
    // assert (Ry == 377'ha0acc5737037be38aeedc80ab62b7389ca50353f69890a73897933f8e09aa81bc753ef50d4376d834c0e85bddf6041);
    
    if (counter == 0) begin
      counter = counter + 1;
      Px = 32;
      Py = 17;
      k = 58;

      Reset = 1'b1;
      #2 Reset = 1'b0;
    end else begin
      $finish;
    end
    
    
    
    
    
  end else
    #1;
end

end

endmodule
