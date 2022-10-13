`timescale 1ns/1ps

module ModAdd #(
  parameter p = 37, // a*b mod p = r
  parameter width = 128 // width of the output
) (
  input clk,
  input reset,
  input [width-1:0] a,        // First multiplication element, a
  input [width-1:0] b,        // Second multiplication element, b
  input enable,
  output [width-1:0] r,         // Remainder, r
  output done
);

  wire [2*width-1:0] a_plus_b;
  assign a_plus_b = {128'b0, a + b};

  ModReduction #(
    .p(p),
    .width(width)
  )
  u_mod_reduction (
      .clk(clk),
      .reset(reset),
      .enable(enable),
      .a(a_plus_b),
      .done(done),
      .r(r)
  );

endmodule