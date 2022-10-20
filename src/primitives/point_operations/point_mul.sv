import elliptic_curve_structs::*;

module point_mul	(
	input logic clk, Reset,
	input curve_point_t  P,
  input logic [255:0] k,
	output logic Done,
	output curve_point_t R
);

// 256-bit counter
logic [255:0] counter;

// Intermediate curves
curve_point_t R_add_temp, R_double_temp, R_temp, Q;

logic reset_add, reset_double, add_done, double_done;


// Consecutively add P to itself k times
point_add p_add(.Reset(Reset | reset_add), .R(R_add_temp), .*);
point_double p_double(.Reset(Reset | reset_double), .R(R_double_temp), .*);

always_ff @ (posedge clk) begin
  if (Reset == 1) begin
    // Global reset
    counter <= k;
    Q <= P;
    R_temp <= P;
    reset_add <= 0;
    reset_double <= 0;
  end else if (reset_add | reset_double) begin
    // Reset adder or doubler
    reset_add <= 0;
    reset_double <= 0;
  end else if (add_done) begin
    // Add done
    counter <= counter - 1;
    R_temp <= R_add_temp;
    reset_add <= 1;
  end else if (double_done) begin
    counter <= counter - 1;
    R_temp <= R_double_temp;
    reset_add <= 1;
  end
  
  else if (k == counter) begin
    // Add point to itself (double)
    reset_double <= 1;
  end else if (k == 0) begin
    // Add initial point to intermediate point
    R <= R_temp;
    Done <= 1;
  end
end


endmodule
