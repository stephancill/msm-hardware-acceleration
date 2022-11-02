
module tb_MultiplierAdapter(

    );

  // Field math example: 123 * 456 + 789 - 123 mod 37
  parameter width = 377;

  reg clk, reset, enable;

  reg signed [width-1:0] a, b;

  wire signed [2*width-1:0] ab;
  wire done;

  wire signed [2*width-1:0] ref = a * b;

  /* 
  * Stage 1: a * b, c - d
  */
  MultiplierAdapter #(
    .width         (width)
  )
  u_multiplier (
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
    a = 377'h12818541fadc53f209e60e2a4648b497d54f933d91e537c643fda3a9f758d56c8d35343053b683f4837b6b35131177a;
    b = 377'h13a6d3b1ea1e9b582d52f1f135bb62eeec445cc6512c7ff4a162209bead94acc8558f28e654f32ee03aee5934019393;
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
          $display("PASS: ref == ab");
        end else begin
          $display("ERROR: ref != ab");
        end
        $finish();
      end
      #10;
    end
  end

    
endmodule