import elliptic_curve_structs::*;

module ModReductionAdapter (
  input   reset,                    // Reset
  input   clk,                    // Clock
  input [2*P_WIDTH-1:0]   a,                      // Number to be reduced, a
  output done,
  output [P_WIDTH-1:0] r            // Remainder, r
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

BarrettReduction u_barrett (
    .reset(reset),                    // Reset
    .clk(clk),                    // Clock
    .a(a),                      // Number to be reduced, a
    .done(done),
    .r(r)            // Remainder, r
  );



endmodule