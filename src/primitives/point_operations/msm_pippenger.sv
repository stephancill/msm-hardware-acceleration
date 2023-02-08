import elliptic_curve_structs::*;

module msm_pippenger #(parameter LENGTH = 256, BUCKETS = 12) (
	input 	logic			clk, Reset,
	input  	curve_point_t G [LENGTH-1:0],
  input   logic [SCALAR_WIDTH-1:0]	x [LENGTH-1:0],
	output 	logic 			Done,
	output 	curve_point_t 	R
);

// States: reset, init, compute, done
localparam reset = 0, populate_B_l_k = 1, compute = 2, done = 3;

localparam K = SCALAR_WIDTH / BUCKETS;


curve_point_t B_lk [LENGTH-1:0][BUCKETS**2-1:0];

logic [$clog2(LENGTH)-1:0] counter_n, counter_k;

logic mul_reset, add_reset, add_done, mul_done;
logic [3:0] state;

curve_point_t R_temp, R_add_temp, R_mul_temp;
logic [SCALAR_WIDTH-1:0] x_i;

point_add                 p_add(.Reset(add_reset), .P(R_temp), .Q(R_mul_temp), .R(R_add_temp), .Done(add_done), .*);
point_mul_double_and_add  p_mul(.Reset(mul_reset), .P(G_i), .k(x_i), .R(R_mul_temp), .Done(mul_done), .*);

//assign Done = counter == (length+1) && add_done && mul_done;
//assign R = R_temp;
//assign l = x[counter]

//// Clock and Reset
//always_ff @(posedge clk) begin
//  if (Reset) begin
//    Done <= 0;
//    R_temp <= inf_point;
//    counter <= 1;
//    add_reset <= 0;
//    mul_reset <= 1;
//    G_i <= G[0];
//    x_i <= x[0];
//    state <= populate_B_l_k;
//  end else begin
//    if (!Done) begin
//      case (state)
//        populate_B_l_k: begin
//          counter <= counter + 1;
//          l <= x[counter] >> ;
//        end 
//        default: 
//      endcase
//    end
//  end
//end

endmodule