import elliptic_curve_structs::*;

module point_mul_double_and_add	(
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

logic reset_add, reset_double;
logic add_done, double_done, stage1_done;

// Consecutively add P to itself k times
point_add p_add(.Reset(reset_add), .P(R_temp), .R(R_add_temp), .Done(add_done), .*);
point_double p_double(.Reset(reset_double), .R(R_double_temp), .Done(double_done), .*);

always_ff @ (posedge clk) begin
  if (Reset == 1) begin
    // Global reset
    $display("reset %d", k);
    counter <= 0;
    Q <= P;
    R_temp <= P;
    reset_add <= 0;
    reset_double <= 0;
    Done <= 0;
    if (k == 1) begin
      R <= P;
      Done <= 1;
    end 
  end else if (!Done) begin
    if (reset_add) begin
      // Reset adder or doubler
      counter <= counter + 1;
      reset_add <= 0;
    end else if (counter == 0) begin
      // Add initial point to intermediate point
      R <= R_temp;
      Done <= 1;
    end else if (add_done) begin
      // Add done
      R_temp <= R_add_temp;
      reset_add <= 1;
    end else if (double_done & ~stage1_done) begin
      R_temp <= R_double_temp;
      reset_add <= 1;
      stage1_done <= 1;
    end
  end
end


endmodule
