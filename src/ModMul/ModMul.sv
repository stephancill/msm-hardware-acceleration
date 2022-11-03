// Source: https://github.com/ingonyama-zk/papers/blob/main/modular_multiplication.pdf
module ModMul (
  input logic clk,
  input logic reset,
  input logic [P_WIDTH-1:0] a,        // First multiplication element, a
  input logic [P_WIDTH-1:0] b,        // Second multiplication element, b
  input logic enable,
  output logic [P_WIDTH-1:0] r,         // Remainder, r
  output logic done
);

  // Option 1:

  logic mul_done, reduction_done;
  logic [2*P_WIDTH-1:0] ab;

  assign done = mul_done & reduction_done;

  ModReductionAdapter u_mod_reduction (
      .clk(clk),
      .reset(reset | ~mul_done),
      .a(ab),
      .done(reduction_done),
      .r(r)
  );

  MultiplierAdapter #(
    .width(P_WIDTH)
  ) u_m1 (
    .clk(clk),
    .reset(reset),
    .enable(enable),
    .a(a),
    .b(b),
    .ab(ab),
    .done(mul_done)
  );

  // -------------------------------------------------

  // Option 2:
  // multiplier mult0(.clk(clk), .Reset(reset), .Done(done), .product(r), .*);

endmodule