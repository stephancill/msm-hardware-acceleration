module tb_BarrettReduction();
 // Field math example: 123 * 456 + 789 - 123 mod 37
  parameter width = 16;
  parameter p = 8'd37;

  reg clk, reset, enable;

  reg signed [2*width-1:0] a;

  wire signed [width-1:0] r;
  wire done;

  wire signed [width-1:0] ref = a % p;

  /* 
  * Stage 1: a * b, c - d
  */
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

  initial begin
    clk = 1'b1;
    #(10/2);
    forever begin
      clk = ~clk;
      #(10/2);
    end
  end
  
  initial begin
    a = 16'd1300;
    #10;
    reset = 1'b1;
    enable = 1'b0;
    #10;
    reset = 1'b0;
    enable = 1'b1;
    
    forever begin
      if (done) begin
        if (ref == r) begin
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