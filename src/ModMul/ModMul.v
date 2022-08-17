// Source: https://github.com/ingonyama-zk/papers/blob/main/modular_multiplication.pdf
`timescale 1ns/1ps
// Calculate r = a * b mod s
module ModMul (
  clk,
  reset,
  s,        // Modulus, s
  m,        // Parameter m = 2 ** (2 * n)
  a,        // First multiplication element, a
  b,        // Second multiplication element, b
  r         // Remainder, r
);

  parameter FIELD_WIDTH = 16; 
  input clk, reset;
  input [FIELD_WIDTH:0] a, b, m;
  input [FIELD_WIDTH-1:0] s;
  output reg [FIELD_WIDTH-1:0] r;

  wire [2*FIELD_WIDTH-1:0] ab = a *b;                   // Full
  wire [3*FIELD_WIDTH:0] l1_full = ab_msb * m;  // TODO: Check if you can't do [3*FIELD_WIDTH:2*FIELD_WIDTH] and avoid intermediary wires
  wire [FIELD_WIDTH+1:0] l1_s_lsb = l1_msb * s;
  wire [FIELD_WIDTH+1:0] r_plus = ab_lsb + ~l1_s_lsb + 1;
  
  wire [FIELD_WIDTH+1:0] ab_msb;    // MSB
  wire [FIELD_WIDTH+1:0] ab_lsb;    // LSB
  wire [FIELD_WIDTH+1:0] l1_msb;

  assign ab_msb = ab[2*FIELD_WIDTH-1:FIELD_WIDTH];
  assign ab_lsb = ab[FIELD_WIDTH+1:0]; 
  assign l1_msb = l1_full[2*FIELD_WIDTH:FIELD_WIDTH];

  always @(r_plus) begin
    r <= r_plus;
  end

  always @(r) begin
    if (r_plus > s) begin
      r = r - s;
    end
  end

  always @(posedge clk) begin
    if (reset) begin
      
    end else begin
      
    end
  end

endmodule