import elliptic_curve_structs::*;

module PointAddAdapter (
	input 	logic 			clk, Reset,
	input  	curve_point_t 	P, Q,
	output 	logic 			Done,
	output 	curve_point_t 	R
);

curve_point_t R_add, R_double;

logic should_double, double_done, add_done;

assign should_double = (P.x == Q.x) && (P.y == Q.y);
assign R = should_double ? R_double : R_add;
assign Done = should_double ? double_done : add_done;

point_add p_add(.Reset(Reset | should_double), .R(R_add), .Done(add_done), .*);
point_double p_double(.Reset(Reset | ~should_double), .R(R_double), .Done(double_done), .*);

endmodule