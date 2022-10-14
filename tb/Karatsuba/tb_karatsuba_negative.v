module tb_karatsuba_negative(

    );

  // Field math example: 123 * 456 + 789 - 123 mod 37
  parameter width = 16;

  reg clk, reset, enable;

  reg signed [width-1:0] a, b;

  wire signed [2*width-1:0] ab;
  wire done;

  wire signed [2*width-1:0] ref = a * b;

  /* 
  * Stage 1: a * b, c - d
  */
  karat_mult_recursion #(
    .wI         (width),
    .nSTAGE     (3)
  )
  u_karat_mult_recursion (
//     input   logic   [wI-1:0]    iX,
// input   logic   [wI-1:0]    iY,
// output  logic   [wO-1:0]    oO,
// // control IOs
// input   logic   clk,
// input   logic   reset,
// input   logic   i_enable,
// output  logic   o_finish
    .iX          (a),
    .iY          (b),
    .oO          (ab),
    .clk         (clk),
    .reset       (reset),
    .i_enable    (enable),
    .o_finish    (done)
    );

  initial begin
    clk = 1'b1;
    #(10/2);
    forever begin
      clk = ~clk;
      #(10/2);
    end
  end
  
  initial begin
    a = 16'd123;
    b = 16'd456;
    #10;
    b = -b;
    reset = 1'b1;
    enable = 1'b0;
    #10;
    reset = 1'b0;
    enable = 1'b1;
    
    forever begin
      if (done) begin
        if (ref == ab) begin
          $display("PASS: r == ab");
        end else begin
          $display("ERROR: r != ab");
        end
        $finish();
      end
      #10;
    end
  end

    
endmodule