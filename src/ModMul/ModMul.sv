// Source: https://github.com/ingonyama-zk/papers/blob/main/modular_multiplication.pdf
`timescale 1ns/1ps
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

  // logic mul_done, reset_reducer, enable_reducer;
  // logic [2*P_WIDTH-1:0] ab;

  // ModReductionAdapter u_mod_reduction (
  //     .clk(clk),
  //     .reset(reset_reducer),
  //     .a(ab),
  //     .done(done),
  //     .r(r)
  // );

  // MultiplierAdapter #(
  //   .width(P_WIDTH)
  // ) u_m1 (
  //   .clk(clk),
  //   .reset(reset),
  //   .enable(enable),
  //   .a(a),
  //   .b(b),
  //   .ab(ab),
  //   .done(mul_done)
  // );

  // always @(posedge clk) begin
  //   if (reset) begin
  //     reset_reducer <= 0;
  //     enable_reducer <= 0;
  //   end else begin
  //     if (mul_done && !enable_reducer) begin
  //       reset_reducer <= 1;
  //       enable_reducer <= 1;
  //     end else begin
  //       reset_reducer <= 0;
  //     end
  //   end
  // end

  // -------------------------------------------------

  // Option 2:
  multiplier mult0(.clk(clk), .Reset(reset), .Done(done), .product(r), .*);

endmodule