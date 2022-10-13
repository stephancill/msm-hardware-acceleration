module ModReduction #(
  parameter p = 37, // a mod p = r
  parameter width = 128 // width of the output
) (
  input   reset,                    // Reset
  input   clk,                    // Clock
  input enable,
  input [2*width-1:0]   a,                      // Number to be reduced, a
  output reg done,
  output wire [width-1:0] r            // Remainder, r
);

reg [2*width-1:0] r_temp;
assign r = r_temp[width-1:0];

always @(clk) begin
  if (reset) begin
    r_temp <= a;
    done <= a < p;
  end else begin
    if (!done & enable) begin
      r_temp = r_temp - p;
      done = r_temp < p;
    end
  end
end



endmodule