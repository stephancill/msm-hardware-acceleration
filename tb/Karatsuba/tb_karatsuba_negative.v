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
  KaratsubaWrapper #(
    .width         (width),
    .stages     (3)
  )
  u_karatsuba_wrapper (
// input clk,
  // input reset,
  // input signed [width-1:0] a,        // First multiplication element, a
  // input signed [width-1:0] b,        // Second multiplication element, b
  // input enable,
  // output signed [2*width-1:0] ab,         // Remainder, r
  // output done
    .a(a),
    .b(b),
    .ab(ab),
    .clk(clk),
    .reset(reset),
    .enable(enable),
    .done(done)
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