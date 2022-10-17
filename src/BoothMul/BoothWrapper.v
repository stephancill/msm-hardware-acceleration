
module BoothWrapper #(
  parameter width = 128 // width of the output
) (
  input clk,
  input reset,
  input signed [width-1:0] a,        // First multiplication element, a
  input signed [width-1:0] b,        // Second multiplication element, b
  input enable,
  output signed [2*width-1:0] ab,         // Remainder, r
  output done
);

reg enabled, ld;

always @(posedge clk) begin
  if (reset) begin
    ld <= 1'b0;
    enabled <= 1'b0;
  end else begin
    if (enable && !enabled) begin
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
    .M(a), 
    .R(b), 
    .Valid(done), 
    .P(ab)
  );

endmodule