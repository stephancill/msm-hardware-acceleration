module tb_BarrettReduction();

parameter p = 128'd37;
parameter wI = 128;
parameter CLK_PERIOD = 10;

reg   [2*wI-1:0]    a;
wire  [wI-1:0]    oO_ref, result;
assign  oO_ref = a % p;

reg   clk, reset, enable;
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
    enable = 1'b0;
    a = 10*p+12;
    enable = 1'b1;
    #(CLK_PERIOD);

    forever begin
        if (done) begin
            if (result == oO_ref) begin
                $display("PASS: result == oO_ref");
                
            end else
            begin
                $display("ERROR: result != oO_ref");
            end
            $finish();
        end 
        #CLK_PERIOD;
      end
end

BarrettReduction #(
    .p(p),
    .width(wI)
)
u_barrett (
    .clk(clk),
    .reset(reset),
    .enable(enable),
    .a(a),
    .done(done),
    .r(result)
);

endmodule