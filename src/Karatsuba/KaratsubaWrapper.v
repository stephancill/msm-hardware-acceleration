
module KaratsubaWrapper #(
  parameter width = 128, // width of the output
  parameter stages = 5
) (
  input clk,
  input reset,
  input signed [width-1:0] a,        // First multiplication element, a
  input signed [width-1:0] b,        // Second multiplication element, b
  input enable,
  output signed [2*width-1:0] ab,         // Remainder, r
  output done
);

wire unsigned [width-1:0] a_abs, b_abs, ab_abs;

assign a_abs = a;
assign b_abs = b;

assign ab = (a < 0) ^ (b < 0) ? -ab_abs : ab_abs;

karat_mult_recursion #(
    .wI         (width),
    .nSTAGE     (stages)
  )
  u_karat_mult_recursion (
    .iX          (a_abs),
    .iY          (b_abs),
    .oO          (ab_abs),
    .clk         (clk),
    .reset       (reset),
    .i_enable    (enable),
    .o_finish    (done)
    );


endmodule