// Source: https://github.com/ingonyama-zk/papers/blob/main/modular_multiplication.pdf
`timescale 1ns/1ps
module ModMul #(
  parameter p = 37, // a*b mod p = r
  parameter width = 128 // width of the output
) (
  input clk,
  input reset,
  input [width-1:0] a,        // First multiplication element, a
  input [width-1:0] b,        // Second multiplication element, b
  output [width-1:0] r,         // Remainder, r
  output reg done
);

  reg mul_done;
  reg [2*width-1:0] ab;
  reg reset_reducer;
  reg enable_reducer;

  always @(posedge clk) begin
    if (reset) begin
      ab <= 0;
      reset_reducer <= 0;
      enable_reducer <= 0;
    end else begin
      if (mul_done) begin
        reset_reducer <= 1;
        enable_reducer <= 1;
      end else begin
        reset_reducer <= 0;
      end
    end
  end
  

  ModReduction #(
    .p(p),
    .width(width)
  )
  u_mod_reduction (
      .clk(clk),
      .reset(reset_reducer),
      .enable(enable_reducer),
      .a(ab),
      .done(done),
      .r(result)
  );

  // Multiplication module
  karat_mult_recursion #(
    .wI         (width),
    .nSTAGE     (5)
  )
  u_karat_mult_recursion (
    // data IOs
    .iX(a),
    .iY(b),
    .oO(ab),
    // control IOs
    .clk(clk),
    .rst_n(reset),
    .i_enable(1),
    .o_finish(mul_done) 
  );

endmodule