import elliptic_curve_structs::*;

module tb_ModMul();

parameter p = params.p;
parameter CLK_PERIOD = 10;

logic   [P_WIDTH-1:0]    a, b;
logic  [P_WIDTH-1:0]    r_ref, r;
logic [P_WIDTH*2-1:0] ab;
assign ab = a * b;
assign  r_ref = ab % p;

logic   clk, reset, i_enable, done;

initial begin
    clk = 1'b1;
    #CLK_PERIOD;
    forever begin
        clk = ~clk;
        #(CLK_PERIOD/2);
    end
end

initial begin
  i_enable = 1'b0;
  #(CLK_PERIOD*5);
  a = 377'h1647170e013bf53a7b050468f43383b17361703bef0431b3f0f3ddad4af519168f4af9b29e96740671f4fbb2b93eb11;
  b = 377'h144b5478f0886377ee7fe272cd4ca5a12f1e38816016588cffe3240b0776a00199763223e90b4b30d4f21c3d098f416;
  
  #CLK_PERIOD;
  reset = 1'b1;
  #CLK_PERIOD;
  reset = 1'b0;
  i_enable = 1'b1;

 forever begin
   if (done) begin
       if (r == r_ref) begin
           $display("PASS: r == r_re");
            
       end else
       begin
           $display("ERROR: r != r_re");
       end
       $finish();
   end 
   #CLK_PERIOD;
 end
end


ModMul #(
   .p(p),
   .width(P_WIDTH)
)
u_modmul (
   .clk(clk),
   .reset(reset),
   .a(a),
   .b(b),
   .enable(i_enable),
   .r(r),
   .done(done)
);

endmodule