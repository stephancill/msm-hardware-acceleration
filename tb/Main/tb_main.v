`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 10/11/2022 09:44:42 PM
// Design Name: 
// Module Name: tb_main
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module tb_main(

    );

  // Field math example: 123 * 456 + 789 - 123 mod 37
  parameter p = 32'd37;
  parameter width = 32;

  reg clk, reset, enable;

  reg [width-1:0] a, b, c, d;

  wire signed [width-1:0] r_ab, r_c_min_d, r_ab_plus_c_min_d;
  wire done_ab, done_c_min_d, done_ab_plus_c_min_d;

  wire stage1_done = done_ab & done_c_min_d;

  wire signed [width-1:0] ref = (r_ab + c - d) % p; // TODO -d

  /* 
  * Stage 1: a * b, c - d
  */
  ModMul #(
    .p(p),
    .width(width)
  ) u_ab (
    .clk(clk),
    .reset(reset),
    .a(a),
    .b(b),
    .enable(enable),
    .r(r_ab),
    .done(done_ab)
  );

  ModAdd #(
    .p(p),
    .width(width)
  ) u_c_min_d (
    .clk(clk),
    .reset(reset),
    .a(c),
    .b(d), // TODO: -d
    .enable(enable),
    .r(r_c_min_d),
    .done(done_c_min_d)
  );


  /* 
  * Stage 2: ab + c - d
  */
  ModAdd #(
    .p(p),
    .width(width)
  ) u_ab_plus_c_min_d (
    .clk(clk),
    .reset(reset),
    .a(r_ab),
    .b(r_c_min_d),
    .enable(stage1_done),
    .r(r_ab_plus_c_min_d),
    .done(done_ab_plus_c_min_d)
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
    a = 32'd123;
    b = 32'd456;
    c = 32'd789;
    d = -32'sd123;
    reset = 1'b1;
    enable = 1'b0;
    #10;
    reset = 1'b0;
    enable = 1'b1;
    
    forever begin
      if (done_ab_plus_c_min_d) begin
        if (ref == r_ab_plus_c_min_d) begin
          $display("PASS: r == r_re");
        end else begin
          $display("ERROR: r != r_re");
        end
        $finish();
      end
      #10;
    end
  end

    
endmodule
