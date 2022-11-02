import elliptic_curve_structs::*;

module tb_BarrettReduction();
 // Field math example: 123 * 456 + 789 - 123 mod 37

  logic clk, reset;

  logic [2*P_WIDTH-1:0] a;

  logic [P_WIDTH-1:0] r;
  logic done;

  logic [P_WIDTH-1:0] verif;
  
  assign verif = a % params.p;

  /* 
  * Stage 1: a * b, c - d
  */
  BarrettReduction u_barrett (
    .reset(reset),                    // Reset
    .clk(clk),                    // Clock
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
    a = 754'h1cf6b5e190d19cd0998015b5af31af5eb6b64eb9163b7745a666cbc3efd3103e56bcb2b10f509cc06844791bec4acbfb03104d3e1103e1bf02436591df74f1fd9323cedccac5de4a2693789bd485f98a3a58d9e0371fdae1675ee5c546e12;
    #10;
    reset = 1'b1;
    #10;
    reset = 1'b0;
    
    forever begin
      if (done) begin
        if (verif == r) begin
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