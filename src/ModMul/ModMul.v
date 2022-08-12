// Source: https://github.com/ingonyama-zk/papers/blob/main/modular_multiplication.pdf

// Calculate r = a * b mod s
module ModMul (
  clk,
  reset,
  n,        // Number of bits to represent element in field F_s
  s,        // Modulus, s
  m,        // Parameter m = 2 ** (2 * n)
  a,        // First multiplication element, a
  b,        // Second multiplication element, b
  r         // Remainder, r
);
  
  input clk, reset;
  input [7:0] n;
  input [n:0] a, b;
  input [n-1:0] s;
  output [n-1:0] r;

  reg [2*n-1:0] ab;   // Full
  wire ab1, ab2;      // MSB, LSB

  assign ab1 = ab[2*n-1:n];
  assign ab2 = ab[n+1:0]; 

  always @(posedge clk) begin
    if (reset) begin
      ab <= 0;
    end else begin
      ab = a * b;
    end
  end

endmodule