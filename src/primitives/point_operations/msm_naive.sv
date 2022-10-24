import elliptic_curve_structs::*;

module msm_naive #(parameter length = 256) (
	input 	logic			clk, Reset,
	input  	curve_point_t G [length-1:0],
  input   logic [255:0]	x [length-1:0],
	output 	logic 			Done,
	output 	curve_point_t 	R
);

logic [$clog2(256)-1:0] counter;

logic mul_reset, add_reset, add_done, mul_done;

curve_point_t R_temp, R_add_temp, R_mul_temp, G_i;
logic [255:0] x_i;

point_add                 p_add(.Reset(add_reset), .P(R_temp), .Q(R_mul_temp), .R(R_add_temp), .Done(add_done), .*);
point_mul_double_and_add  p_mul(.Reset(mul_reset), .P(G_i), .k(x_i), .R(R_mul_temp), .Done(mul_done), .*);

assign Done = counter == (length-1) && add_done && mul_done;

// Clock and Reset
always_ff @(posedge clk) begin
  if (Reset) begin
    Done <= 0;
    R_temp <= inf_point;
    counter <= 0;
    add_reset <= 0;
    mul_reset <= 1;
    G_i <= G[0];
    x_i <= x[0];
  end else begin
    if (!Done) begin
      if (mul_reset) begin
        mul_reset <= 0;
      end else if (add_reset) begin
        add_reset <= 0;
      end else if (mul_done) begin
        add_reset <= 1;
      end else if (add_done && mul_done) begin
        counter <= counter + 1;
        mul_reset <= 1;
        R_temp <= R_add_temp;
        G_i <= G[counter];
        x_i <= x[counter];
      end
    end
  end
end



endmodule