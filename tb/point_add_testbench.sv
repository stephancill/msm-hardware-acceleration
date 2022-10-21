//openssl ec -in ecprivkey.pem -pubout -out ecpubkey.pem
module point_add_testbench();

timeunit 10ns;	// Half clock cycle at 50 MHz
			// This is the amount of time represented by #1
timeprecision 1ns;

logic clk, Reset;
logic [255:0] Py, Qy, Px, Qx, Rx, Ry;
logic Done;

point_add uncreative_name(.P({Px, Py}), .Q({Qx, Qy}), .R({Rx, Ry}), .*);
// Toggle the clock
// #1 means wait for a delay of 1 timeunit
always begin : CLOCK_GENERATION
#1 clk = ~clk;
end

initial begin: CLOCK_INITIALIZATION
    clk = 0;
end

//Testing
initial begin: TEST_VECTORS
//Initialize signals
Reset = 1'b1;
#2 Reset = 1'b0;
Px = 4'd6;
Py = 4'd1;
Qx = 4'd8;
Qy = 4'd1;

forever begin
    if (Done) begin
        assert (Rx == 23);
        assert (Ry == 36);
        $finish;
    end else
        #1;
end
end

endmodule
