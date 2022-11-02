
module KaratsubaWrapper #(
  parameter width = 128 // width of the output
) (
  input clk,
  input reset,
  input [width-1:0] a,        // First multiplication element, a
  input [width-1:0] b,        // Second multiplication element, b
  input enable,
  output [2*width-1:0] ab,         // Remainder, r
  output done
);

localparam stages = $clog2(width) - 3;
localparam localwidth = 2**$clog2(width);

wire [localwidth-1:0] a_local, b_local;

assign a_local = a;
assign b_local = {{(localwidth-width){1'b0}}, b};

// wire unsigned [width-1:0] a_abs, b_abs, ab_abs;

// assign a_abs = a[width-1] ? -a : a; // First bit is sign bit
// assign b_abs = b[width-1] ? -b : b;

// assign ab = a[width-1] ^ b[width-1] ? -ab_abs : ab_abs;

always @(clk) begin
  if (reset)
    $display("stages: %d, localwidth: %d", stages, localwidth);
end

karat_mult_recursion #(
    .wI         (localwidth),
    .nSTAGE     (stages)
  )
  u_karat_mult_recursion (
    .iX          (a_local),
    .iY          (b_local),
    .oO          (ab),
    .clk         (clk),
    .reset       (reset),
    .i_enable    (enable),
    .o_finish    (done)
    );


endmodule