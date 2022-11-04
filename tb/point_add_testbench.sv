//openssl ec -in ecprivkey.pem -pubout -out ecpubkey.pem
module point_add_testbench();

timeunit 10ns;	// Half clock cycle at 50 MHz
			// This is the amount of time represented by #1
timeprecision 1ns;

logic clk, Reset;
logic [P_WIDTH-1:0] Py, Qy, Px, Qx, Rx, Ry;
logic Done;

point_add padd(.P({Px, Py}), .Q({Qx, Qy}), .R({Rx, Ry}), .*);
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
// Px = 377'h116a2c0f839d9608121202ed49d41a2fb23252aa7ae75c60ad61d9cf807e53ff10ba3ff99bf43ff6c8bfbbc6528a33b;
// Py = 377'h10bd644104333b1a8dbdf058a5136c194b1ff7e9731969156a8c4dfd46446cd5d93a2de3130da01999d9072585ff593;
// Qx = 377'h15cb2b78125751fb25b7414331049db03171d64163d3e4d7f24d1b49a7dec64b7556430086a8cd5cf7e0538b54e5aae;
// Qy = 377'hda2ff1d86d14ac58e419e9dc65ffdabf150a885dad5e7a9fb67241f54eb899f963e749d0cc3eee2281231e05461396;

Px = 6;
Py = 1;
Qx = 32;
Qy = 17;

forever begin
    if (Done) begin
        // assert (Rx == 'h11d0606bfe4dd39c34390e3a47c4ac9b9d8c7fb0d91e4bc74f45331e7906339d051cca0bd781fcaa198e1e946e08e8f);
        // assert (Ry == 'h214efdc19577de50b18ee9cadd843e9d055e706485fe221a382d4a02c48b2ddc8de32394077dbf860cd38e63cf135d);
        // Check if point R is (32, 20)
        if (Rx == 32 && Ry == 20) begin
            $display("Test passed");
        end else begin
            $display("Test failed");
        end
        $finish;
    end else
        #1;
end
end

endmodule
