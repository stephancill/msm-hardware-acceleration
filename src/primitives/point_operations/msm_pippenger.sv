import elliptic_curve_structs::*;

module msm_naive #(parameter length = 256) (
	input 	logic			clk, Reset,
	input  	curve_point_t G [length-1:0],
  input   logic [255:0]	x [length-1:0],
	output 	logic 			Done,
	output 	curve_point_t 	R
);



endmodule