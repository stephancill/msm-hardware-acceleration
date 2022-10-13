module tb_ModAdd();

parameter p = 128'd37;
parameter wI = 128;
parameter CLK_PERIOD = 10;

reg   [wI-1:0]    a, b;
wire  [wI-1:0]    r_ref, r;
assign  r_ref = (a + b) % p;

reg   clk, reset, i_enable;
wire done;

initial begin
    clk = 1'b1;
    reset = 1'b1;
    #CLK_PERIOD;
    reset = 1'b0;
    #CLK_PERIOD;
    forever begin
        clk = ~clk;
        #(CLK_PERIOD/2);
    end
end

initial begin
  i_enable = 1'b0;
  #(CLK_PERIOD*5);
  a = 128'd123;
  b = 128'd456;
  i_enable = 1'b1;
  #CLK_PERIOD;

  reset = 1'b1;
  #CLK_PERIOD;
  reset = 1'b0;
  #CLK_PERIOD;

 forever begin
  if (done) begin
      if (r == r_ref) begin
        $display("PASS: r == r_re");
      end else begin
        $display("ERROR: r != r_re");
      end
      $finish();
  end 
  #CLK_PERIOD;
 end
end


ModAdd #(
   .p(p),
   .width(wI)
)
u_modadd (
   .clk(clk),
   .reset(reset),
   .a(a),
   .b(b),
   .enable(i_enable),
   .r(r),
   .done(done)
);

endmodule