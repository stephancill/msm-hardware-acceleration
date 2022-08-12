// Source: https://github.com/ingonyama-zk/papers/blob/main/modular_multiplication.pdf

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

  parameter FIELD_WIDTH = 16; // Number of bits to represent element in field F_s
  
  input clk, reset;
  input [FIELD_WIDTH:0] a, b, m;
  input [FIELD_WIDTH-1:0] s;
  output [FIELD_WIDTH-1:0] r;

  reg [2*FIELD_WIDTH-1:0] ab;   // Full
  wire ab1, ab2;      // MSB, LSB

  assign ab1 = ab[2*FIELD_WIDTH-1:FIELD_WIDTH];
  assign ab2 = ab[FIELD_WIDTH+1:0]; 

  always @(posedge clk) begin
    if (reset) begin
      ab <= 0;
    end else begin
      ab = a * b;
    end
  end

endmodule