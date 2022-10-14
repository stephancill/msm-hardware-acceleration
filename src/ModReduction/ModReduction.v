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

reg enabled;
reg [2*width-1:0] r_temp;
assign r = r_temp[width-1:0];

always @(clk) begin
  if (reset) begin
    // Global reset
    enabled <= 1'b0;
  end else begin
    if (enable & !enabled) begin
      // Local reset on enable
      r_temp <= a;
      done <= a < p;
      enabled <= 1'b1;
    end

    if (!done & enabled) begin
      r_temp = r_temp - p;
      done = r_temp < p;
    end
  end
end

endmodule