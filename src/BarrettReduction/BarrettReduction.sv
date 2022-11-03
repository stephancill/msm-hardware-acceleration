import elliptic_curve_structs::*;

module BarrettReduction (
  input   reset,  clk,
  input logic [2*P_WIDTH-1:0] a,                      // Number to be reduced, a
  output logic done,
  output logic [P_WIDTH-1:0] r            // Remainder, r (reffered to as t in the paper)
);

// Precomputed factor floor(4^k / p)
localparam [2*P_WIDTH+1:0] mask = {1'b1,{P_WIDTH{1'b0}}, {P_WIDTH{1'b0}}};
localparam [P_WIDTH:0] q = mask / params.p;
logic enable, m1_done, m2_done, sub_done;

logic [3*P_WIDTH-1:0] t1; // a * q
logic [P_WIDTH-1:0] t2;
logic [2*P_WIDTH-1:0] t3; // t2 * p
logic [P_WIDTH:0] t4;

assign t2 = t1 >> (2*P_WIDTH);


MultiplierAdapter #(
  .width(2*P_WIDTH)
) u_m1 (
  .clk(clk),
  .reset(reset),
  .enable(enable),
  .a(a),
  .b({{P_WIDTH{1'b0}}, q}),
  .ab(t1),
  .done(m1_done)
);

MultiplierAdapter #(
  .width(P_WIDTH)
) u_m2 (
  .clk(clk),
  .reset(reset),
  .enable(m1_done),
  .a(t2),
  .b({{P_WIDTH{1'b0}}, params.p}),
  .ab(t3),
  .done(m2_done)
);

always_ff @( clk ) begin
  if ( reset ) begin
    r <= 0;
    enable <= 1;
    t4 <= 0;
    sub_done <= 0;
    done <= 0;
  end else begin
    if (!done) begin
      if (m2_done && m1_done) begin
        if (!sub_done) begin
          t4 <= a - t3;
          sub_done <= 1;
        end else begin
          if (t4 < params.p) begin
            r <= t4;
            done <= 1;
          end else begin
            r <= t4 - params.p;
            done <= 1;
          end
        end
    end
  end
end
end

endmodule