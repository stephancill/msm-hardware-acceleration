module TestHarnass_tb;

// Inputs
logic clk;
logic rst;

// Outputs
logic done;
//logic out;

// Instance of the design under test (DUT)
TestHarnassModMul uut (
.clk(clk),
.rst(rst),
.done(done)
//.out(out)
);

// Clock period
parameter CLK_PERIOD = 10;

// Initialize simulation inputs
initial begin
  clk = 0;
  rst = 1;
  #(CLK_PERIOD*8) rst = 0;
end

// Generate clock
always #(CLK_PERIOD/2) clk = ~clk;

// Check outputs
initial begin
  #(CLK_PERIOD * 10)
  if (done) begin
    $display("Operation is done");
//    $display("out = %d", out);
    $finish;
  end
end

endmodule