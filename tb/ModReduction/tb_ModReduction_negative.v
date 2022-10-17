module tb_ModReduction_negative();

parameter p = 128'sd37;
parameter wI = 128;
parameter CLK_PERIOD = 10;

reg signed   [2*wI-1:0]    a;
wire signed [wI-1:0]    oO_ref, result;
assign  oO_ref = a < 0 ? a % p + p : a % p;

reg   clk, rst_n, i_enable;
wire done;

initial begin
    clk = 1'b1;
    rst_n = 1'b1;
    #CLK_PERIOD;
    rst_n = 1'b0;
    #CLK_PERIOD;
    forever begin
        clk = ~clk;
        #(CLK_PERIOD/2);
    end
end

initial begin
    i_enable = 1'b0;
    a = -10*p+12;
    i_enable = 1'b1;
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

ModReduction #(
    .p(p),
    .width(wI)
)
u_mod_reduction (
    .clk(clk),
    .reset(rst_n),
    .enable(i_enable),
    .a(a),
    .done(done),
    .r(result)
);

endmodule