// Generic multiplier interface which can be used to control the 
// multiplication module to be used

module MultiplierAdapter #(
  parameter width = 128 // width of the output
) (
  input clk,
  input reset,
  input signed [width-1:0] a,        // First multiplication element, a
  input signed [width-1:0] b,        // Second multiplication element, b
  input enable,
  output signed [2*width-1:0] ab,         // Remainder, r
  output done
);

  // Chosen multiplication module
  // KaratsubaWrapper #(
  //   .width         (width),
  //   .stages     (2)
  // )
  // u_karatsuba_wrapper (
  //   .a(a),
  //   .b(b),
  //   .ab(ab),
  //   .clk(clk),
  //   .reset(reset),
  //   .enable(enable),
  //   .done(done)
  //   );

  BoothWrapper #(
    .width         (width)
  ) u_booth_multiplier (
    .a(a),
    .b(b),
    .ab(ab),
    .clk(clk),
    .reset(reset),
    .enable(enable),
    .done(done)
    );
  
endmodule