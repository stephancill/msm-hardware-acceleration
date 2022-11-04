import elliptic_curve_structs::*;

module msm_naive #(parameter length = 256) (
	input 	logic			clk, Reset,
	input  	curve_point_t G [length-1:0],
  input   logic [SCALAR_WIDTH-1:0]	x [length-1:0],
	output 	logic 			Done,
	output 	curve_point_t 	R
);

logic [$clog2(length):0] counter;

logic mul_reset, add_done, mul_done;

curve_point_t R_temp, R_add_temp, R_mul, R_mul_temp, G_i;
logic [SCALAR_WIDTH-1:0] x_i;

PointAddAdapter           p_add(.Reset(Reset | ~mul_done), .P(R_temp), .Q(R_mul_temp), .R(R_add_temp), .Done(add_done), .*);
point_mul_double_and_add  p_mul(.Reset(Reset | mul_reset), .P(G_i), .k(x_i), .R(R_mul_temp), .Done(mul_done), .*);

assign Done = counter == length;
assign R = R_temp;
assign G_i = G[counter];
assign x_i = x[counter];

// Clock and Reset
always_ff @(posedge clk) begin
  if (Reset) begin
    Done <= 0;
    R_temp <= inf_point;
    R_mul <= inf_point;
    mul_reset <= 1;
    counter <= 0;
  end else begin
    if (!Done) begin
      if (mul_reset) begin
        mul_reset <= 0;
      end else if (~add_done && mul_done) begin
        R_mul <= R_mul_temp;
      end else if (add_done && mul_done) begin
        $display("counter= %d r_temp.x = %d", counter, R_temp.x);
        mul_reset <= 1;
        R_temp <= R_add_temp;
        counter <= counter + 1;
      end
    end
  end
end



endmodule