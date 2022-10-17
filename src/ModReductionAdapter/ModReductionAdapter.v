module ModReductionAdapter #(
  parameter signed p = 37, // a mod p = r
  parameter width = 128 // width of the output
) (
  input   reset,                    // Reset
  input   clk,                    // Clock
  input enable,
  input signed [2*width-1:0]   a,                      // Number to be reduced, a
  output reg done,
  output wire signed [width-1:0] r            // Remainder, r
);



endmodule