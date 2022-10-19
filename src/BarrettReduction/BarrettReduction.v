module BarrettReduction #(
  parameter integer p = 128'd37, // a mod p = r
  parameter width = 128 // width of the output
) (
  input   reset,                    // Reset
  input   clk,                    // Clock
  input enable,
  input signed [2*width-1:0]   a,                      // Number to be reduced, a
  output reg done,
  output wire signed [width-1:0] r            // Remainder, r (reffered to as t in the paper)
);

  // Requirement: a < p^2
  // https://www.nayuki.io/page/barrett-reduction-algorithm
  localparam integer n_2 = width * 2;
  localparam [2*width:0] r_ = (1'b1 << n_2) / p;  // TODO: Fix this check this maybe: https://github.com/ljhsiun2/EllipticCurves_SystemVerilog/blob/master/src/primitives/modular_operations/barrett_reduction.sv

  wire signed [3*width-1:0] abr;
  wire [width-1:0] abr_div4_k = abr >> n_2;
  wire [2*width-1:0] abr_div4_k_times_p;
  // t = ab - abr_div4_k_times_p
  reg [width-1:0] t;
  assign r = t;

  wire m1_done, m2_done;

  MultiplierAdapter #(
    .width(2*width)
  ) u_m1 (
    .clk(clk),
    .reset(reset),
    .enable(enable),
    .a(a),
    .b(r_),
    .ab(abr),
    .done(m1_done)
  );

  MultiplierAdapter #(
    .width(width)
  ) u_m2 (
    .clk(clk),
    .reset(reset),
    .enable(m1_done),
    .a(abr_div4_k),
    .b(p),
    .ab(abr_div4_k_times_p),
    .done(m2_done)
  );

  always @(posedge clk ) begin
    if (reset) begin
      t <= 0;
      done <= 0;
    end else if (enable) begin
      if (m1_done && m2_done && !done) begin
        t = a - abr_div4_k_times_p;
        $display("t=%d, p=%d", t, p);
        if (t >= p) begin
          $display("t >= p");
          t <= t - p;
          done <= 1;
        end else begin
          $display("t < p");
          done <= 1;
        end
      end
    end
  end







  
endmodule