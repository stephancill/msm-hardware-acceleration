module BarrettReduction #(
  parameter signed p = 128'b37, // a mod p = r
  parameter width = 128 // width of the output
) (
  input   reset,                    // Reset
  input   clk,                    // Clock
  input enable,
  input signed [2*width-1:0]   a,                      // Number to be reduced, a
  output reg done,
  output wire signed [width-1:0] r            // Remainder, r
);

  localparam m = 2**(2*width) / p;

  wire [width-1:0] s = p;

  wire [2*width-1:0] ab = a;                   // Full
  wire [3*width:0] l1_full; // = ab_msb * m;  // TODO: Check if you can't do [3*width:2*width] and avoid intermediary wires
  wire [width+1:0] l1_s_lsb; // = l1_msb * s;
  wire [width+1:0] r_plus;
  
  wire [width+1:0] ab_msb;    // MSB
  wire [width+1:0] ab_lsb;    // LSB
  wire [width+1:0] l1_msb;

  assign ab_msb = ab[2*width-1:width];
  assign ab_lsb = ab[width+1:0]; 
  assign l1_msb = l1_full[2*width:width];

  assign r = r_plus[width-1:0];

  wire m1_done, m2_done, a1_done;

  MultiplierAdapter #(
    .width         (width)
  )
  u_m1 (
    .a(ab_msb),
    .b(m),
    .ab(l1_full),
    .clk(clk),
    .reset(reset),
    .enable(enable),
    .done(m1_done)
    );

  // TODO: Use single multiplier
  MultiplierAdapter #(
    .width         (width)
  )
  u_m2 (
    .a(l1_msb),
    .b(s),
    .ab(l1_s_lsb),
    .clk(clk),
    .reset(reset),
    .enable(m1_done),
    .done(m2_done)
    );

  always @(posedge clk) begin
    if (reset) begin
      state <= WAITING_FOR_NEW;
      m1_done <= 1'b0;
      m2_done <= 1'b0;
    end else begin
      if (enable) begin
        if (m2_done && !a1_done) begin
          r_plus <= ab_lsb + ~l1_s_lsb + 1;
          a1_done <= 1'b1;
        end else if (a1_done && !done) begin
          r_plus = r_plus - s;
          done = r_plus < s;
        end
      end
    end
  end
  
endmodule