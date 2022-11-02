import elliptic_curve_structs::*;

module BoothWrapper #(
  parameter width = 128
) (
  input logic clk,
  input logic reset,
  input logic [width-1:0] a,        // First multiplication element, a
  input logic [width-1:0] b,        // Second multiplication element, b
  input logic enable,
  output logic [2*width-1:0] ab,         // Remainder, r
  output logic done
);

localparam padding = 2**$clog2(width) - width;

logic enabled, ld;



always @(posedge clk) begin
  if (reset) begin
    ld <= 1'b0;
    enabled <= 1'b0;
  end else begin
    if (!enabled && enable) begin
      ld <= 1'b1;
      enabled <= 1'b1;
    end else begin
      ld <= 1'b0;
    end
  end
end

Booth_Multiplier    #(
    .pN($clog2(width))
  ) u_booth (
    .Rst(reset), 
    .Clk(clk), 
    .Ld(ld), 
    .M({{padding{1'b0}}, a}), 
    .R({{padding{1'b0}}, b}), 
    .Valid(done), 
    .P(ab)
  );

endmodule