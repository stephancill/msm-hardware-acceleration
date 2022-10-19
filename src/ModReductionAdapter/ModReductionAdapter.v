module ModReductionAdapter #(
  parameter signed p = 37, // a mod p = r
  parameter width = 128 // width of the output
) (
  input   reset,                    // Reset
  input   clk,                    // Clock
  input enable,
  input signed [2*width-1:0]   a,                      // Number to be reduced, a
  output done,
  output wire signed [width-1:0] r            // Remainder, r
);


// ModReduction #(
//   .p(p),
//   .width(width)
//   ) u_mod_reduction (
//     .clk(clk),
//     .reset(reset),
//     .enable(enable),
//     .a(a),
//     .done(done),
//     .r(r)
//   );

BarrettReduction #(
    .p(p),
    .width(width)
  ) u_barrett (
    .reset(reset),                    // Reset
    .clk(clk),                    // Clock
    .enable(enable),
    .a(a),                      // Number to be reduced, a
    .done(done),
    .r(r)            // Remainder, r
  );



endmodule