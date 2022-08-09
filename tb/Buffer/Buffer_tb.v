`timescale 1ns/1ns
`include "../../src/Buffer/Buffer.v"

module Buffer_tb;

reg A;
wire B;

Buffer dut(.A(A), .B(B));

initial begin
  $dumpfile("dump.vcd");
  $dumpvars(0, Buffer_tb);

  A = 0;
  #20;
  A = 1;
  #20;
  A = 0;
  #20;

  $display("Done");
end

endmodule