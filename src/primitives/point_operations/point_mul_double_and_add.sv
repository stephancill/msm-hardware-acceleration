import elliptic_curve_structs::*;

module point_mul_double_and_add	(
	input logic clk, Reset,
	input curve_point_t  P,
  input logic [width-1:0] k,
	output logic Done,
	output curve_point_t R
);

localparam width = 254;

// 256-bit counter
logic [$clog2(width)-1:0] counter;


// Intermediate curve points
curve_point_t R_add_temp, R_double_temp, R_temp, J;

logic local_reset, add_done, double_done, should_add;

assign should_add = k[counter];
assign Done = counter == width && double_done && (add_done || !should_add); // TODO: Update this
assign R = R_temp;

// Double-and-add method
point_add     p_add(.Reset(local_reset), .P(R_temp), .Q(J), .R(R_add_temp), .Done(add_done), .*);
point_double  p_double(.Reset(local_reset), .P(J), .R(R_double_temp), .Done(double_done), .*);

always_ff @ (posedge clk) begin
  if (Reset == 1) begin
    // Global reset
    counter <= 0;
    J <= P;
    R_temp <= inf_point;
    local_reset <= 1;
    Done <= 0;
    if (k == 1) begin
      R <= P;
      Done <= 1;
    end 
  end else if (!Done) begin
    if (local_reset) begin
      local_reset <= 0;
    end else if (double_done & (add_done || ~should_add)) begin
      counter <= counter + 1;
      local_reset <= 1 && (counter + 1 != width);
      J <= R_double_temp;
      if (should_add) begin
        R_temp <= R_add_temp;
      end
    end
  end
end


endmodule
